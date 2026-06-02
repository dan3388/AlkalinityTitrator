import time

from titration.devices.library import (
    Keypad,
    PHProbe,
    StirControl,
    SyringePump,
    TemperatureControl,
    TemperatureProbe,
    Heater
)
hcl_volume = 0

def run_hardware_test():
    print("--- Alkalinity Titrator: Standalone Hardware Test ---")
    print("Initializing hardware...")
    
    try:
        pump = SyringePump()
        print("pump done")
        ph_probe = PHProbe()
        print("PH probe done")
        stir_controller = StirControl()
        print("Stir control done")
        keypad = Keypad()
        print("keypad done")
        stir_controller.set_stop()
        temp_probe = TemperatureProbe(2)
        print("Temp probe done")
        heater = Heater(12)
        print("Heater done")
        control = TemperatureControl(temp_probe, heater)
        print("Control done")
        print("Hardware initialized successfully.\n")
    except Exception as e:
        print(f"Failed to initialize hardware: {e}")
        return

    print("=== Manual Titration Loop ===")
    while True:
        # 1. Read pH
        print("\nReading pH...")
        volts = ph_probe.get_voltage()
        print(f"Current pH Voltage: {volts:>4.5f} V")
        
        # 2. Ask for volume to move
        print("\nEnter volume to move in ml (e.g., 0.1), or type 'q' to quit:")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'q':
            print("Exiting test...")
            break
            
        try:
            volume = float(user_input)
        except ValueError:
            print("Invalid volume. Please enter a number.")
            continue
            
        # 3. Ask for direction
        print(f"\nMoving {volume} ml. Choose direction:")
        print("0: Refill")
        print("1: Push Volume Out")
        direction = input("> ").strip()
        
        if direction == '0':
            print(f"[Hardware] Pulling {volume} ml in...")
            pump.refill(volume)
        elif direction == '1':
            print(f"[Hardware] Pushing {volume} ml out...")
            pump.dispense(volume)
        else:
            print("Invalid direction. Skipping pump action.")
            continue
            
        # 4. Stir/Degas
        print("\nStir to mix? (y/n)")
        stir = input("> ").strip().lower()
        if stir == 'y':
            print("Enter stir time in seconds (e.g., 5):")
            stir_input = input("> ").strip()
            try:
                stir_time = float(stir_input)
                print(f"[Hardware] Stirring for {stir_time} seconds...")
                stir_controller.set_slow()
                time.sleep(stir_time)
                stir_controller.set_stop()
                print("[Hardware] Stirring complete.")
            except ValueError:
                print("Invalid time. Skipping stir.")
        
        print(f"\nDispensed {hcl_volume}mL of HCl\n")
        print(f"-------*---------*-------*---------*-------*---------")

if __name__ == "__main__":
    try:
        run_hardware_test()
    except KeyboardInterrupt:
        print("\nTest terminated by user.")
