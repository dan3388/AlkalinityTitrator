import board
import busio

print("Initializing SPI Bus...")
# Match the pins from your temperature_probe.py
spi = busio.SPI(board.D11, MOSI=board.D10, MISO=board.D9)

# We must lock the bus before we can send raw data
while not spi.try_lock():
    pass

try:
    # Configure basic SPI settings
    spi.configure(baudrate=9600, phase=0, polarity=0)
    print("SPI Bus Locked and Configured.\n")

    # The test pattern we are sending (0xAA is 10101010 in binary, a great test wave)
    send_data = bytearray([0xAA, 0x55, 0x00, 0xFF])
    
    # An empty buffer to catch whatever comes back
    receive_data = bytearray(len(send_data))

    print(f"Sending:  {[hex(b) for b in send_data]}")

    # This commands the Pi to shout and listen at the exact same time
    spi.write_readinto(send_data, receive_data)

    print(f"Received: {[hex(b) for b in receive_data]}\n")

    if send_data == receive_data:
        print("SUCCESS: SPI Loopback Passed!")
        print("Your Pi, OS, PCB traces, and SPI hardware are PERFECT.")
    else:
        print("FAILED: Data mismatch.")
        print("MISO did not hear what MOSI sent.")

finally:
    spi.unlock()
    print("\nSPI Bus Unlocked.")
