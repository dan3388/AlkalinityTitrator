import time
import board
import busio
import digitalio
from adafruit_max31865 import MAX31865

print("Initializing SPI and Sensor...")
spi = busio.SPI(board.D11, MOSI=board.D10, MISO=board.D9)
cs = digitalio.DigitalInOut(board.D4)

# Initialize the sensor
sensor = MAX31865(spi, cs, rtd_nominal=1000, ref_resistor=4300.0, wires=2)

# 1. Read the raw uncalculated integer from the ADC
raw_adc = sensor.read_rtd()
print(f"Raw ADC Value (0-32767): {raw_adc}")

# 2. Read the Fault Register
fault = sensor.fault
print(f"Internal Fault Register: {fault}")

if raw_adc == 0 and not fault:
    print("\nDIAGNOSIS: REALITY A (Silent Chip)")
    print("The chip is not talking to the Pi. You have a broken MISO trace right at the chip, or the chip has no power.")
elif fault:
    print("\nDIAGNOSIS: REALITY B (Screaming Chip)")
    print("The SPI bus is PERFECT! The chip is alive but it sees a physical short in your resistor wiring.")


while True:
	temp = sensor.temperature
	print(f"temp: {temp:0.2f}")
	time.sleep(1)
