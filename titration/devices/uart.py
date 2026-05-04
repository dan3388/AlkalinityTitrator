# from titration.devices.library import Serial
from titration.devices.library import Serial
import time

class UART:
    def __init__(self, port='/dev/serial0', baudrate=115200):
        self.ser = Serial(port, baudrate=baudrate, timeout=1)
        time.sleep(0.1)

    def send_command(self, cmd):
        self.ser.write((cmd+"\n").encode('utf-8'))
        print("Sent: {cmd}")

        line = self.ser.readline().decode('utf-8').rstrip()
        if line:
            print(f"Pico Response: {line}")
            return line
        return None
    
    def read_message(self):
        if self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').rstrip()
            return line
        return None
