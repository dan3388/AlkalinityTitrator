"""
The file to configure mock objects
"""

# pylint: disable=unused-import, ungrouped-imports, wrong-import-position
# mypy: ignore-errors

from titration import mock_config

# if mock_config.MOCK_ENABLED:
#     from titration.mock import ads_mock as ADS
#     from titration.mock import analog_mock as analog_in
#     from titration.mock import board_mock as board
#     from titration.mock import i2c_mock as busio
#     from titration.mock import pwm_out_mock as pwmio
#     from titration.mock.digital_mock import DigitalInOut
#     from titration.mock.heater_mock import Heater
#     from titration.mock.keypad_mock import Keypad
#     from titration.mock.liquid_crystal_mock import LiquidCrystal
#     from titration.mock.max31865_mock import MAX31865
#     from titration.mock.serial_mock import Serial
#     from titration.mock.spi_mock import SPI
# else:
import adafruit_ads1x15.ads1115 as ADS
import board
import busio
import pwmio
from adafruit_ads1x15 import analog_in
from adafruit_max31865 import MAX31865
from busio import SPI
from digitalio import DigitalInOut
from gpiozero import LED as Heater
from serial import Serial
from titration.devices.keypad import Keypad
from titration.devices.liquid_crystal import LiquidCrystal
from titration.devices.uart import UART
from titration.devices.ph_probe import PHProbe
from titration.devices.stir_control import StirControl
from titration.devices.syringe_pump import SyringePump
from titration.devices.data_collector import DataCollector
from titration.devices.temperature_control import TemperatureControl
from titration.devices.temperature_probe import TemperatureProbe
