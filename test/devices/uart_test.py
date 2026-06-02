from titration.devices.library import UART
import time

uart = UART(
    port='/dev/serial0',
    baudrate=9600,
    timeout=15
)

while True:
    # Check initial status
    uart.send_command("STAT")
    print("Requested status")
    time.sleep(2)

    # Dispense 0.1 mL
    uart.send_command("P_OUT:0.1")
    print("Dispensing 0.1 mL")
    time.sleep(5)

    # Check status again
    uart.send_command("STAT")
    print("Requested status")
    time.sleep(2)

    # Dispense 0.25 mL
    uart.send_command("P_OUT:0.25")
    print("Dispensing 0.25 mL")
    time.sleep(5)

    # Check status again
    uart.send_command("STAT")
    print("Requested status")
    time.sleep(2)

    # Refill syringe
    uart.send_command("P_IN")
    print("Refilling syringe")
    time.sleep(10)  # Allow time for refill

    # Final status check
    uart.send_command("STAT")
    print("Requested status")
    time.sleep(5)
