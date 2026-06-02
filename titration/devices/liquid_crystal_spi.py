"""
The file for the Sunfire LCD 20x04 Char Display using Adafruit I2C/SPI LCD Backpack, LiquidCrystalSPI Class
"""
import time

import board
import busio
import digitalio
import adafruit_character_lcd.character_lcd_spi as character_lcd


LCD_WIDTH = 20
LCD_HEIGHT = 4

class LiquidCrystalSPI:
    """
    The class for the Sunfire LCD 20x04 Char Display via SPI
    """

    def __init__(self, latch_pin=board.D19, clock_pin=board.D21, data_pin=board.D20):
        """
        The constructor for the SPI LiquidCrystal class.
        
        Parameters:
            latch_pin: The board pin connected to the latch (LAT) pin of the SPI backpack.
        """
        self.cols = LCD_WIDTH
        self.rows = LCD_HEIGHT

        # Initialize SPI bus (SCK and MOSI are used for the backpack)
        self.spi = busio.SPI(clock_pin, MOSI=data_pin)
        
        # Initialize Latch pin
        self.latch = digitalio.DigitalInOut(latch_pin)
        
        # Initialize the LCD class from adafruit_character_lcd
        self.lcd = character_lcd.Character_LCD_SPI(self.spi, self.latch, self.cols, self.rows)

        # Toggle backlight on-off-on to indicate initialization
        self.lcd_backlight(True)
        time.sleep(0.5)
        self.lcd_backlight(False)
        time.sleep(0.5)
        self.lcd_backlight(True)
        time.sleep(0.5)

    def clear(self):
        """
        The function to clear the LCD
        """
        self.lcd.clear()

    def print(self, message, line, style="left"):
        """
        The function to send a string to the LCD on a given line and type

        Parameters:
            message (string): the message to be displayed on the screen
            line (int): the line to display the message on (1-indexed)
            style (string): 1=left centered, 2=centered, 3=right centered
                           (matches "left", "center", "right")
        """
        if self.cols == -1 or self.rows == -1:
            raise ValueError("The LCD has not been initialized")

        if style == "left":
            message = message.ljust(self.cols, " ")
        elif style == "center":
            message = message.center(self.cols, " ")
        elif style == "right":
            message = message.rjust(self.cols, " ")

        row = line - 1
        if 0 <= row < self.rows:
            self.lcd.cursor_position(0, row)
            self.lcd.message = message

    def lcd_backlight(self, enable):
        """
        The function to turn the LCD backlight on or off

        Parameters:
            enable (bool): enable is whether the lcd_backlight is on or off
        """
        self.lcd.backlight = enable

    def display_list(self, dict_to_display):
        """
        The function to display a list of options from a dictionary.
        Only the first four options will be displayed due to only four screen rows.

        Parameters:
            dict_to_display (dict): list to be displayed on LCD screen
        """
        self.clear()
        keys = list(dict_to_display.keys())
        values = list(dict_to_display.values())
        lines = [1, 2, 3, 4]

        for i in range(min(len(keys), 4)):
            self.print(str(keys[i]) + ". " + values[i], lines[i])
