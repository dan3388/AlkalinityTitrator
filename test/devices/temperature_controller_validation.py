import time
import board
from titration.devices.library import TemperatureControl,Heater, TemperatureProbe

probe = TemperatureProbe(2)
heater = Heater(12)
print("Temperature controller object created")
control = TemperatureControl(probe, heater)
time.sleep(5)

print("Controller Activated")
control.activate()
start_time = time.time()
cont = True
while cont:
	control.update()
	temp = probe.get_temperature()
	val = heater.value
	state = "on" if val else "off"
	print(f"Time: {(time.time() - start_time):.2f}s | Temperature: {temp:0.2f} | Heater: {state} | Gain: {control.k:0.2f}")
	time.sleep(0.5)
	if (time.time() - start_time) == 900:
		control.deactivate()
		cont = False
print("Test done")
