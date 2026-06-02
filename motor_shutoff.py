import board 
import pwmio

motor = pwmio.PWMOut(board.D13, duty_cycle=0, frequency=100)
motor.deinit()
print("Motor Off")
