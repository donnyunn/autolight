import odroid_wiringpi as wpi
from threading import Thread
import time

wpi.wiringPiSetup()

coil_A_1_pin = 4
coil_A_2_pin = 21
coil_B_1_pin = 23
coil_B_2_pin = 11

wpi.pinMode(coil_A_1_pin, 1)
wpi.pinMode(coil_A_2_pin, 1)
wpi.pinMode(coil_B_1_pin, 1)
wpi.pinMode(coil_B_2_pin, 1)

StepCount = 8
Seq = list(range(0, StepCount))
Seq[0] = [0,0,0,1]
Seq[1] = [0,0,1,1]
Seq[2] = [0,0,1,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,1,0,0]
Seq[5] = [1,1,0,0]
Seq[6] = [1,0,0,0]
Seq[7] = [1,0,0,1]

busy = False

def setStep(w1, w2, w3, w4):
    wpi.digitalWrite(coil_A_1_pin, w1)
    wpi.digitalWrite(coil_A_2_pin, w2)
    wpi.digitalWrite(coil_B_1_pin, w3)
    wpi.digitalWrite(coil_B_2_pin, w4)

def release():
    setStep(0, 0, 0, 0)

def forward_work(steps):
    global busy
    for i in list(range(steps)):
        for j in list(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(0.001)
    release()
    busy = False

def forward(cycle):
    global busy
    if busy is False:
        busy = True
        t = Thread(target = forward_work, args = (cycle,))
        t.start()

def backwards_work(steps):
    global busy
    for i in list(range(steps)):
        for j in reversed(list(range(StepCount))):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(0.001)
    release()
    busy = False

def backward(cycle):
    global busy
    if busy is False:
        busy = True
        t = Thread(target = backwards_work, args = (cycle,))
        t.start()

# def bye():
#     GPIO.cleanup()
    
if __name__ == '__main__':
    while True:
        steps = input("How many steps forward? ")
        forward(int(steps))
        steps = input("How many steps backwards? ")
        backward(int(steps))