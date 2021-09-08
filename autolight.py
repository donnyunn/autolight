#!/usr/bin/env python
from __future__ import print_function

import numpy as np
import cv2 as cv
import stepper as step
# import led

# local modules
from video import create_capture
from common import clock, draw_str

X_RESOLUTION = 480
Y_RESOLUTION = 320

click = False

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10),
                                     flags=cv.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    if len(rects) is 1:
        for x1, y1, x2, y2 in rects:
            # cv.line(img, ((x1+x2)/2, 0), ((x1+x2)/2, 360), color, 1, 4 )
            # cv.line(img, (0, (y1+y2)/2), (640, (y1+y2)/2), color, 1, 4 )
            cv.rectangle(img, (x1, y1), (x2, y2), color, 2)
            return (x1+x2)/2, (y1+y2)/2
    # else:
    #     for x1, y1, x2, y2 in rects:
    #         cv.rectangle(img, (x1, y1), (x2, y2), color, 2)
    return 0, 0
def mouseEvent(event, x, y, flags, param):
    global click
    if event == cv.EVENT_LBUTTONUP:
        click = True

@static_vars(cnt=0)
def decision(vis, x, lum):
    print("led.setDuty(%d)"%(255-lum))
    # led.setDuty(255 - lum)

    if x != 0:
        decision.cnt += 1
    else:
        decision.cnt = 0

    origin = X_RESOLUTION/2
    margin = 10
    if decision.cnt > 1:
        if abs(x - origin) > margin:
            if x >= origin:
                # print("step.forward(4)")
                step.forward(4)
            else:
                # print("step.backward(4)")
                step.backward(4)

def main():
    import sys, getopt

    global click

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade='])
    try:
        video_src = video_src[0]
    except:
        video_src = -1
        
    args = dict(args)
    cascade_fn = args.get('--cascade', "/home/odroid/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
    cascade = cv.CascadeClassifier(cv.samples.findFile(cascade_fn))

    cam = create_capture(video_src, fallback='synth:bg={}:noise=0.05'.format(cv.samples.findFile('/home/odroid/opencv/samples/data/lena.jpg')))
    
    cam.set(cv.CAP_PROP_FRAME_WIDTH, X_RESOLUTION)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, Y_RESOLUTION)

    t = clock()
    while True:
        ret, img = cam.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        rects = detect(gray, cascade)
        vis = img.copy()
        x, y = draw_rects(vis, rects, (0, 255, 0))

        dt = clock() - t
        t = clock()
        lum = np.average(vis)

        draw_str(vis, (20, 20), '%.1f ms' % (dt*1000))
        draw_str(vis, (20, 40), '%.1f' % lum)
        if x is not 0:
            draw_str(vis, (20, 60), '%d' % x)

        decision(vis, x, lum)
        
        cv.line(vis, (240, 0), (240, 320), (0, 0, 255), 1, 1)
        cv.imshow('facedetect', vis)
        cv.setMouseCallback('facedetect', mouseEvent)

        if cv.waitKey(5) == 27:
            break
        if click:
            break
    
    # step.bye()
    # led.bye()
    print('Done')

if __name__ == '__main__':
    print('Face Detection Start')
    main()
    cv.destroyAllWindows()