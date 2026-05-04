"""
The file for the SyringePump class
"""
from titration.devices.library import Serial, UART

MAX_PUMP_CAPACITY = 1.1
NUM_CYCLES = {0.05: 470, 1: 9550}

class SyringePump:
    """
    The class for the Syringe Pump device
    
    UART Messages:
    PUSH_X: Send to Pico to dispense X*0.05 mL of Acid 
    ADDV_X: Receive from Pico to add X*0.05mL to the volume_dispenseds
    """

    def __init__(self):
        """
        The constructor function for the syringe pump
        Initializes the arduino to control the pump motor
        """
        self.uart = UART()
        self.volume_dispensed = 0

    def update_volume(self):
        while True:
            message = self.uart.read_message()
            if message is None:
                break
            if message and message.startswith("ADDV_"):
                self.volume_dispensed += 0.05

    def push_volume_out(self, amt):
        message = "PUSH_" + str(amt) + "\n"
        self.uart.send_command(message)

