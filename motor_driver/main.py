from machine import Pin, UART
import time

# --- Math Constants ---
STEPS_PER_0_05_ML = 1240
ML_PER_STEP = 0.05 / STEPS_PER_0_05_ML
STEPS_PER_ML = int(1 / ML_PER_STEP)  # 24800

class Stepper:
    def __init__(self, step_pin, dir_pin, en_pin, limit_fwd_pin, limit_bwd_pin, solenoid_pin):
        # Initialize Motor Pins
        self.step = Pin(step_pin, Pin.OUT)
        self.direction = Pin(dir_pin, Pin.OUT)
        self.enable = Pin(en_pin, Pin.OUT)
        
        # Initialize Limit Switches
        self.limit_forward = Pin(limit_fwd_pin, Pin.IN, Pin.PULL_UP)
        self.limit_backward = Pin(limit_bwd_pin, Pin.IN, Pin.PULL_UP)
        
        # Initialize Solenoid (To switch between reservoir and titration beaker)
        self.solenoid = Pin(solenoid_pin, Pin.OUT)
        
        # Initial Safe State
        self.enable.value(1)  # Disable motor initially
        self.direction.value(0)
        self.step.value(0)
        self.solenoid.value(0)
        
        # Statistics & State Tracking
        self.max_syringe_vol_ml = 5.0  # Adjust this to your syringe's actual max volume
        self.current_vol_ml = self.max_syringe_vol_ml
        self.total_dispensed_ml = 0.0

    def dispense(self, volume_ml):
        """Pushes X amount out of the syringe (P_OUT)"""
        if volume_ml <= 0:
            return
            
        steps = int(volume_ml * STEPS_PER_ML)
        
        print(f"Dispensing {volume_ml}mL ({steps} steps)...")
        self.solenoid.value(1)  # Route fluid to titration beaker
        time.sleep_ms(100)      # Wait for solenoid to actuate
        
        self.enable.value(0)
        self.direction.value(0) # Forward
        time.sleep_ms(50)
        
        actual_steps = 0
        for _ in range(steps):
            # Safety check: Stop immediately if forward limit switch is hit
            if self.limit_forward.value() == 0:
                print("WARNING: Forward limit reached prematurely.")
                break
                
            self.step.value(1)
            time.sleep_us(500)
            self.step.value(0)
            time.sleep_us(500)
            actual_steps += 1
            
        self.enable.value(1)
        
        # Update statistics based on actual distance moved
        actual_volume = actual_steps * ML_PER_STEP
        self.current_vol_ml -= actual_volume
        self.total_dispensed_ml += actual_volume

    def refill(self):
        """Pulls liquid into the tubes until limit switch is triggered (P_IN)"""
        print("Refilling syringe...")
        self.solenoid.value(0)  # Route fluid to pull from reservoir
        time.sleep_ms(100)      # Wait for solenoid to actuate
        
        self.enable.value(0)
        self.direction.value(1) # Backward
        time.sleep_ms(50)
        
        # Keep stepping backward until the backward limit switch goes LOW (pressed)
        while self.limit_backward.value() != 0:
            self.step.value(1)
            time.sleep_us(500)
            self.step.value(0)
            time.sleep_us(500)
            
        self.enable.value(1)
        
        # Reset current volume to maximum since we hit the back limit
        self.current_vol_ml = self.max_syringe_vol_ml
        print("Refill complete.")


class UARTComm:
    def __init__(self, tx_pin=0, rx_pin=1, baudrate=9600):
        # Initialize UART
        self.uart = UART(0, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.buffer = ""

    def send_response(self, message):
        """Sends string back to the Raspberry Pi"""
        self.uart.write(message + "\n")

    def get_commands(self):
        """Reads from UART and returns a list of parsed commands, if any."""
        commands = []
        if self.uart.any():
            data = self.uart.read()
            if data:
                try:
                    text = data.decode("utf-8")
                    for ch in text:
                        if ch == '\n' or ch == '\r':
                            command = self.buffer.strip()
                            self.buffer = ""
                            if command:
                                commands.append(command)
                        else:
                            self.buffer += ch
                except Exception as e:
                    self.send_response("ERROR:DECODE_FAIL")
        return commands


# ==========================================
# Main Execution Loop (The Orchestrator)
# ==========================================
def main():
    print("Initializing Titrator Motor RTS...")
    
    # Initialize classes
    # Assuming GPIO 5 for Solenoid. Change if needed.
    stepper = Stepper(step_pin=4, dir_pin=3, en_pin=2, 
                      limit_fwd_pin=21, limit_bwd_pin=22, solenoid_pin=16)
    
    comm = UARTComm(tx_pin=0, rx_pin=1, baudrate=9600)
    
    print("System Ready. Waiting for commands (P_OUT:X, P_IN, STAT)...")

    while True:
        # 1. Ask UART for any fully formed commands
        commands = comm.get_commands()
        
        # 2. Process commands and trigger the Stepper class
        for cmd in commands:
            print(f"Received: {cmd}")
            
            if cmd.startswith("P_OUT:"):
                try:
                    # Extract the X value from "P_OUT:X"
                    vol_str = cmd.split(":")[1]
                    volume_to_push = float(vol_str)
                    
                    stepper.dispense(volume_to_push)
                    comm.send_response(f"OK:DISPENSED:{volume_to_push}")
                except Exception as e:
                    comm.send_response("ERROR:BAD_POUT_VALUE")
                    
            elif cmd == "P_IN":
                stepper.refill()
                comm.send_response("OK:REFILLED")
                
            elif cmd == "STAT":
                # Respond with formatted data
                dispensed = round(stepper.total_dispensed_ml, 4)
                current = round(stepper.current_vol_ml, 4)
                comm.send_response(f"STAT:DISPENSED={dispensed},CURRENT_VOL={current}")
                
            else:
                comm.send_response("ERROR:UNKNOWN_COMMAND")
            
        # Small delay to yield to the processor
        time.sleep(0.01)

if __name__ == "__main__":
    main()
