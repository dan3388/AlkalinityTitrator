"""
The file for the SyringePump class
"""
from titration.devices.uart import UART

PUMP_CAPACITY = 1.0  

class SyringePump:
    """
    The class for the Syringe Pump device communicating with the Pico RTS
    """

    def __init__(self):
        # Increased timeout to 30s. Refilling a full syringe can take time!
        self.uart = UART(port='/dev/serial0', baudrate=9600, timeout=30)
        self.volume_in_pump = PUMP_CAPACITY
        self.get_status()

    def get_status(self):
        """Queries the Pico for actual volume states to keep Pi in sync."""
        response = self.uart.send_command("STAT")
        if response and response.startswith("STAT:"):
            # Example response: "STAT:DISPENSED=1.05,CURRENT_VOL=3.95"
            try:
                parts = response.split(',')
                current_vol_str = parts[1].split('=')[1]
                self.volume_in_pump = float(current_vol_str)
            except Exception as e:
                print(f"Warning: Failed to parse STAT from Pico: {e}")

    def set_volume_in_pump(self, volume):
        self.volume_in_pump = volume

    def dispense(self, volume_to_add):
        """
        Pushes volume_to_add out of the syringe.
        Returns the volume that was NOT moved (e.g. if limit switch is hit early).
        """
        if volume_to_add == 0:
            return 0
            
        if volume_to_add < 0:
            # If a negative value is passed, trigger a full refill.
            self.refill()
            return 0

        # 1. Get exact volume before move
        self.get_status()
        start_vol = self.volume_in_pump
        
        # 2. Send dispense command
        command = f"P_OUT:{volume_to_add}"
        response = self.uart.send_command(command)
        
        if response is None:
            raise Exception("RTS Error: Serial Timeout (Pump took too long or disconnected)")
        elif response.startswith("ERROR"):
            raise Exception(f"RTS Error from Pico: {response}")
            
        # 3. Get exact volume after move to calculate the true amount moved
        self.get_status()
        end_vol = self.volume_in_pump
        
        actual_volume_moved = start_vol - end_vol
        missed_volume = volume_to_add - actual_volume_moved
        
        # Prevent tiny floating point math errors from looking like missed steps
        if abs(missed_volume) < 0.001:
            return 0
            
        return missed_volume

    def empty(self):
        """Pushes out all remaining fluid."""
        self.get_status()
        # Push current volume + 0.1mL extra to guarantee the limit switch is hit
        self.dispense(self.volume_in_pump + 0.1) 

    def refill(self):
        """Pulls plunger back to refill from the reservoir."""
        response = self.uart.send_command("P_IN")
        
        if response is None:
            raise Exception("RTS Error: Serial Timeout during refill")
        elif response.startswith("OK:REFILLED"):
            self.volume_in_pump = PUMP_CAPACITY
            self.get_status() # Sync with Pico one last time
        else:
            raise Exception(f"RTS Error during refill: {response}")
