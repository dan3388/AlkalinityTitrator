import serial
import time

class UART:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=15):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(0.1)

    def send_command(self, cmd):
        """Sends a command and immediately waits for the Pico's response."""
        self.ser.write((cmd + "\n").encode('utf-8'))
        print(f"Sent: {cmd}")  

        # Wait for response (will block until \n is received OR timeout is hit)
        line = self.ser.readline().decode('utf-8').strip()
        
        if line:
            print(f"Pico Response: {line}")
            return line
            
        print("Pico Response: TIMEOUT")
        return None
    
    def read_message(self):
        """Non-blocking read for unexpected messages."""
        if self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8').strip()
            return line
        return None
    