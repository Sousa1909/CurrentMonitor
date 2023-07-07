# Script to test if the sensor works

import time
import machine

current = machine.ADC(0)

while True:
    value = current.read_u16()
    print(value)
    time.sleep(3)

