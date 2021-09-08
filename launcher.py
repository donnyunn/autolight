import time, os
import threading

def facetest():
    time.sleep(10)
    os.system('python /home/pi/facetest/facetest.py')

time.sleep(10)

t = threading.Thread(target=facetest)
t.start()

print('thread started')