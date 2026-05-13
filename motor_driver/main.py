from machine import Pin, UART
import time
import sys

# CONSTANTS AND GPIO PINS
T_ON = 500  # Time in us
RX_PIN = 0
TX_PIN = 1
ENABLE_PIN = 2
DIR_PIN = 3
STEP_PIN = 4
LIM_1 = 21
LIM_0 = 22
SOL_PIN = 16

# Setting all Pins
step = Pin(STEP_PIN, Pin.OUT)
direction = Pin(DIR_PIN, Pin.OUT)
enable = Pin(ENABLE_PIN, Pin.OUT)
solenoid = Pin(SOL_PIN, Pin.OUT)
lim1 = Pin(LIM_1, Pin.IN, Pin.PULL_DOWN)
lim0 = Pin(LIM_0, Pin.IN, Pin.PULL_DOWN)

uart = UART(0, baudrate=9600, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

def initialize():
    enable.value(1) # Disable stepper motor
    direction.value(1) # Set direction to default
    solenoid.value(0) # Default solenoid off
    step.value(0)
    
def limit_checker():
    # Returns True if either limit switch is triggered
    return lim0.value() == 1 or lim1.value() == 1

def execute_move(dir_val, cycles):
    """
    Executes an exact number of cycles requested by the Pi 4B.
    Returns the number of cycles REMAINING if a limit switch is hit.
    Returns 0 if successful.
    """
    # 1. Set Hardware Direction and Solenoid based on requested direction
    # Assuming dir_val 1 = Dispense (Push), dir_val 0 = Refill (Draw)
    if dir_val == 1:
        direction.value(1)
        solenoid.value(1) # Route to beaker
    else:
        direction.value(0)
        solenoid.value(0) # Route to reagent bottle
        
    time.sleep_ms(50) # Give solenoid time to actuate

    enable.value(0) # Enable motor
    steps_taken = 0
    
    # 2. Step the motor
    for i in range(cycles):
        if limit_checker():
            # STOP immediately. Motor has hit the end.
            enable.value(1)
            solenoid.value(0)
            return cycles - steps_taken # Return how many steps we FAILED to do

        step.value(1)
        time.sleep_us(T_ON)
        step.value(0)
        time.sleep_us(T_ON)
        steps_taken += 1

    # 3. Clean up and report success
    enable.value(1)
    solenoid.value(0)
    return 0

# --- MAIN RTS LOOP ---
initialize()

while True:
    if uart.any():
        try:
            # Read the incoming string from Pi 4B
            line = uart.readline().decode('utf-8').strip()
            
            # Expected format: "MOVE:DIR:CYCLES" (e.g., "MOVE:1:9550")
            if line.startswith("MOVE"):
                parts = line.split(":")
                req_dir = int(parts[1])
                req_cycles = int(parts[2])
                
                # Execute and get result
                remaining_cycles = execute_move(req_dir, req_cycles)
                
                # Handshake back to the Pi 4B
                if remaining_cycles == 0:
                    uart.write("DONE\n")
                else:
                    # Send back the exact number of cycles missed so Pi 4B can fix its math
                    uart.write(f"{remaining_cycles}\n")
                    
        except Exception as e:
            # If parsing fails or invalid data arrives, flush it out
            uart.write("ERROR\n")
            continue