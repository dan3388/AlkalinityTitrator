# CONSTANTS AND GPIO PINS
T_ON = 500 # Time in us
N_STEP = 950 # 0.05 mL theoretically. More testing needed. 
RX_PIN = 0
TX_PIN = 1
ENABLE_PIN = 2
DIR_PIN = 3
STEP_PIN = 4
LIM_1 = 21
LIM_0 = 22
SOL_PIN = 16

from machine import Pin, UART
import time
import sys

# Setting all Pins and UART
step = Pin(STEP_PIN, Pin.OUT)
direction = Pin(DIR_PIN, Pin.OUT)
enable = Pin(ENABLE_PIN, Pin.OUT)
solenoid = Pin(SOL_PIN, Pin.OUT)
lim1 = Pin(LIM_1, Pin.IN, Pin.PULL_DOWN)
lim0 = Pin(LIM_0, Pin.IN, Pin.PULL_DOWN)

uart = UART(0, baudrate=115200, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

def initialize():
    enable.value(1) #Disable stepper motor
    direction.value(1) #Set direction to 1
    solenoid.value(0) #default solenoid is 0
    uart.write("Stepper motor is set")

def limit_checker():
    if lim0.value() == 1 or lim1.value() == 1:
        return 1
    return 0

def process_cmd(cmd):
    if "PUSH" in cmd:
        push_liquid()
        uart.write("Syringe Pushed\n")
    elif "SOLENOID_ON" in cmd:
        uart.write("Solenoid activated\n")

#give argument to decide direction and solenoid 
def change_direction():
    solenoid.value(1)
    direction.value(0)

def push_liquid(times):
    # Push liquid by 0.05mL increments 
    for i in range(times):
        push_5U()
    
    
def push_5U():
    # Stepper motor function that will activate stepper motor N_STEP steps
    # Roughly 0.05mL 
    enable.value(0)
    for i in range(N_STEP):
        if limit_checker() == 1:
            uart.write("ERR_0\n")
            draw_liquid()
        step.value(1)
        time.sleep_us(T_ON)
        step.value(0)
        time.sleep_us(T_ON)
    enable.value(1)
    uart.write("ADDV_\n") # Inform Titration that 0.05mL were added

def draw_liquid():
    # Refilling the syringle completely 
    # Change direction in the solenoid and motor for drawing HCl
    solenoid.value(0) 
    direction.value(0) 
    
    # Motor stepping until limit switch hit
    enable.value(0) 
    while not limit_checker():
        step.value(1)
        time.sleep_us(T_ON)
        step.value(0)
        time.sleep_us(T_ON)
    enable.value(1)

    # Change motor and solenoid direction back  
    solenoid.value(1)
    direction.value(1)