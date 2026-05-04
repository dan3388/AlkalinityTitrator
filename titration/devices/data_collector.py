"""
Class collecting data from ph-probe and temperature sensor.
"""

# from devices.library import PHProbe
# from devices.library import TemperatureProbe

class DataCollector:
    def __init__(self, filename):
        self.filename = filename
        self.f = None
    
    def __enter__(self):
        self.f = open(self.filename, "w")
        self.f.write("pH,Temperature\n")  # Header
        return self

    def write_data(self, ph_value, temperature):
        if self.f:
            data = f"{ph_value},{temperature}\n"
            self.f.write(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.f:
            self.f.close()

if __name__ == "__main__":
    with DataCollector("data.csv") as collector:
        for i in range(10):
            temp = 30 + i % 2
            collector.write_data(i, temp)
    