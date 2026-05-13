"""
The file for the SyringePump class
"""
from titration.devices.uart import UART 

CYCLES_VOLUME_RATIO = 9550 
PUMP_CAPACITY = 1.0  # in mL

class SyringePump:
    """
    The class for the Syringe Pump device
    """

    def __init__(self):
        # Initialize your custom UART. 
        self.uart = UART(port='/dev/serial0', baudrate=9600, timeout=15)
        self.volume_in_pump = 0

    def set_volume_in_pump(self, volume):
        self.volume_in_pump = volume

    def pump_volume(self, volume_to_add):
        if volume_to_add == 0:
            return 0
            
        cycles = int(volume_to_add * CYCLES_VOLUME_RATIO)
        direction = 1 if volume_to_add > 0 else 0
        
        offset = self.__drive_step_stick(abs(cycles), direction)
        
        if offset != 0:
            actual_cycles_moved = abs(cycles) - offset
            actual_volume_moved = actual_cycles_moved / CYCLES_VOLUME_RATIO
            
            if direction == 0:
                self.volume_in_pump = PUMP_CAPACITY 
            else:
                self.volume_in_pump = 0             
                
            return volume_to_add - (actual_volume_moved * (1 if direction == 1 else -1))
            
        self.volume_in_pump -= volume_to_add
        return 0

    def empty_syringe(self):
        self.pump_volume(PUMP_CAPACITY * 1.1)

    def fill_syringe(self):
        self.pump_volume(-PUMP_CAPACITY * 1.1)

    def __drive_step_stick(self, cycles, direction):
        if cycles == 0:
            return 0

        command = f"MOVE:{direction}:{cycles}"
        response = self.uart.send_command(command)
        
        if response == "DONE":
            return 0
        elif response is None:
            raise Exception("RTS Error: Serial Timeout (Pump took too long or disconnected)")
        else:
            try:
                # Limit switch hit, returning missed steps
                return int(response)
            except ValueError:
                raise Exception(f"RTS Error: Unrecognized response '{response}'")