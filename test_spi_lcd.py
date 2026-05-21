import time
import board
from titration.devices.liquid_crystal_spi import LiquidCrystalSPI

def run_test():
    print("Initializing SPI LCD...")
    
    # Using D5 as the latch pin. Change this to match your wiring!
    # The default SPI pins for Raspberry Pi are SCK (SCLK) and MOSI.
    try:
        lcd = LiquidCrystalSPI(latch_pin=board.D5=19)
    except Exception as e:
        print(f"Failed to initialize LCD: {e}")
        print("Make sure you have installed the required library: pipenv install adafruit-circuitpython-charlcd")
        return

    print("Clearing screen...")
    lcd.clear()
    time.sleep(1)

    print("Testing print to different lines and alignments...")
    lcd.print("Hello World!", 1, style="center")
    time.sleep(1)
    
    lcd.print("Left align", 2, style="left")
    time.sleep(1)
    
    lcd.print("Right align", 3, style="right")
    time.sleep(1)
    
    lcd.print("SPI Backpack Works!", 4, style="center")
    time.sleep(3)

    print("Testing dictionary display_list...")
    menu = {
        1: "Option A",
        2: "Option B",
        3: "Option C",
        4: "Option D"
    }
    lcd.display_list(menu)
    time.sleep(3)

    print("Testing backlight toggle...")
    for i in range(3):
        lcd.lcd_backlight(False)
        time.sleep(0.5)
        lcd.lcd_backlight(True)
        time.sleep(0.5)

    print("Clearing and exiting...")
    lcd.clear()
    lcd.print("Test Complete", 2, style="center")
    time.sleep(2)
    lcd.clear()

if __name__ == "__main__":
    run_test()
