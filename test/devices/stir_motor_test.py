import time
from titration.devices.library import StirControl, DigitalInOut, board


stir_motor = StirControl()
print("Setting Fast")
stir_motor.set_fast()
time.sleep(5)
print("Setting Stop")
stir_motor.set_stop()
time.sleep(5)
print("Setting Slow")
stir_motor.set_slow()
time.sleep(5)
print("Setting Stop")
stir_motor.set_stop()
time.sleep(5)

def run_stir_motor_test():
    print("--- Starting Stir Motor Hardware Test ---")
    try:
        # Test Fast Speed
        print("Ramping up to FAST speed (PWM 5000) for 5 seconds...")
        stir_motor.set_fast()
        time.sleep(5)
        
        # Test Slow Speed
        print("Dropping to SLOW speed (PWM 3000) for 5 seconds...")
        stir_motor.set_slow()
        time.sleep(5)
        
        # Test Degas Sequence and Timer
        print("Testing DEGAS function (simulating a 5-second degas timer)...")
        stir_motor.degas(5)
        
        # Poll the timer to verify the countdown logic works
        for _ in range(6):
            print(f"Degas time remaining: {stir_motor.get_timer()}")
            time.sleep(1)
            
        # Stop Motor
        print("Stopping motor...")
        stir_motor.set_stop()
        print("--- Test Complete ---")
        
    except Exception as e:
        print(f"Hardware Error! An exception occurred: {e}")
        print("Checklist:")
        print("1. Are you running this on the Raspberry Pi with the correct GPIO privileges?")
        print("2. Is the motor controller signal pin securely connected to D13?")
        print("3. Does the motor driver have proper power and common ground with the Pi?")


run_stir_motor_test()
