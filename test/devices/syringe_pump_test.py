import time
from titration.devices.syringe_pump import SyringePump

def run_hardware_test():
    print("="*50)
    print("Starting Syringe Pump Hardware Test")
    print("="*50)

    try:
        # 1. Initialization
        print("\n[1] Initializing SyringePump Object...")
        pump = SyringePump()
        print(f"Success! Current recorded volume in pump: {pump.volume_in_pump} mL")

        # 2. Test Dispense
        dispense_amt = 0.1
        print(f"\n[2] Testing Dispense: Pushing {dispense_amt} mL...")
        missed = pump.dispense(dispense_amt)
        print(f"Dispense complete. Missed volume: {missed} mL.")
        print(f"Current recorded volume in pump: {pump.volume_in_pump} mL")
        
        time.sleep(2) # Brief pause so you can observe the physical pump

        # 3. Test Emptying
        print("\n[3] Testing Emptying: Pushing remaining fluid out...")
        pump.empty()
        print("Emptying complete.")
        print(f"Current recorded volume in pump: {pump.volume_in_pump} mL")
        
        time.sleep(2)

        # 4. Test Refilling
        print("\n[4] Testing Refill: Pulling fluid back in...")
        pump.refill()
        print("Refill complete.")
        print(f"Current recorded volume in pump: {pump.volume_in_pump} mL")

        print("\n" + "="*50)
        print("All hardware tests completed successfully!")
        print("="*50)

    except Exception as e:
        print("\n!!! ERROR ENCOUNTERED DURING TEST !!!")
        print(str(e))

run_hardware_test()
