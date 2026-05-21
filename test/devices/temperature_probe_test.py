"""
The file to test the mock temperature sensor
"""

from titration.devices.library import TemperatureProbe
from titration.devices.max31865_mock import MAX31865Mock # Or import your real driver
import time

def create_temperature_probe(probe_number):
    """
    The function to create a mock temperature sensor
    """
    return TemperatureProbe(probe_number)


def test_temperature_probe_one_create():
    """
    The function to test creating the first mock temperature probe
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor is not None


def test_temperature_probe_two_create():
    """
    The function to test creating the second mock temperature probe
    """
    temperature_sensor = create_temperature_probe(2)
    assert temperature_sensor is not None


def test_get_temperature():
    """
    The function to test getting a temperature from the mock sensor
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor.get_temperature() == 0


def test_get_resistance():
    """
    The function to test getting a resistance from a mock sensor
    """
    temperature_sensor = create_temperature_probe(1)
    assert temperature_sensor.get_resistance() == 100



# Initialize your probe
probe = TemperatureProbe(1)

print("Starting sensor data stream... (Ctrl+C to stop)")
try:
    while True:
        # Fetch the temperature from the PT1000
        temp = probe.get_temperature()
        print(f"Current Temperature: {temp:.2f} °C")
        
        
        time.sleep(1) # Read once per second
except KeyboardInterrupt:
    print("\nData stream stopped.")