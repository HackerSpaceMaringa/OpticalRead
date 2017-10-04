# Verificar direcao predominante em vetores

import argparse
import numpy as np
import cv2
import sys
import thread
import time

from math import *
from OSC import OSCClient, OSCMessage

ap = argparse.ArgumentParser()
ap.add_argument("--verbose", action="store_true", help="Print data")
ap.add_argument("-v", "--video", help="Path of the video")
ap.add_argument("-c", "--camera", type=int, default=0, help="Id of the camera")
ap.add_argument("-s", "--span", type=int, default=25, help="Span between the points")
ap.add_argument("-max", "--max-threshold", type=int, default=60, help="Maximum threshold to send")
ap.add_argument("-min", "--min-threshold", type=int, default=10, help="Minimum threshold to send")
ap.add_argument("-i", "--ip", default="localhost", help="Ip of the OSC receiver server")
ap.add_argument("-p", "--port", type=int, default=7110, help="Port of the OSC receiver server")
args = vars(ap.parse_args());

Span = args.get("span", None)
MinThreshold = args.get("min_threshold", None)
MaxThreshold = args.get("max_threshold", None)

FpsState = False
ColorState = False
rConst = 50
gConst = 50
bConst = 50

Ip = args.get("ip", None)
Port = args.get("port", None)

if args.get("video", None) is None:
    Camera = cv2.VideoCapture(args.get("camera", None))
else:
    Camera = cv2.VideoCapture(args.get("video", None))

if args['verbose']:
    def verbosePrint(*args):
        for arg in args:
            print arg,
        print
else:   
    verbosePrint = lambda *a: None

LkParam = { 
        'winSize': (50, 50),
        'maxLevel': 1,
        'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
            10, 0.03)
        }

Height, Width = (0, 0)

font = cv2.FONT_HERSHEY_SIMPLEX

client = OSCClient()
client.connect((Ip, Port))

def getFixedPoints(Height, Width):
    PrevL = np.arange(Span, Height, Span)
    PrevC = np.arange(Span, Width, Span)
    LenL = len(PrevL)
    LenC = len(PrevC)
    PrevL = np.repeat(PrevL, LenC)
    PrevC = np.tile(PrevC, LenL)
    Prev = np.array([PrevL, PrevC]).T
    Prev = np.array([[[I[1], I[0]]] for I in Prev], dtype=np.float32)
    return Prev

def invert(Pt):
    return (Pt[0] * -1, Pt[1])

def distance(Pt1, Pt2):
    dist = pow((Pt2[0] - Pt1[0]), 2) + pow((Pt2[1] - Pt1[1]), 2)
    return sqrt(dist)

def getSlope(Pt1, Pt2):
    Pt1 = invert(Pt1)
    Pt2 = invert(Pt2)

    DistX = Pt2[0] - Pt1[0]
    DistY = Pt2[1] - Pt1[1]

    return DistY / DistX

def getAngle(Pt1, Pt2):
    Dist = distance(Pt1, Pt2) 
    DistX = Pt2[0] - Pt1[0]
    DistY = Pt2[1] - Pt1[1]

    Degree = 180 - degrees(acos(DistX / Dist))
    if (DistY < 0):
        return Degree
    elif (DistY > 0):
        return 360 - Degree

    if (DistX >= 0):
        return 180
    else:
        return 0

def getDistColor(dist):
    return ((dist * rConst) % 256, (dist * gConst) % 256, (dist * bConst) % 256)

def calculateFPS(start, end):
    return int(1/(end - start))

def sendData(type, message):
    client.send( OSCMessage(type, message) )
    verbosePrint(Vec)

start = time.time()
Last = np.array([])
while True:
    Tuple = Camera.read()
    if Tuple[0]:

        Img = Tuple[1]
        GImg = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)

        if len(Last) == 0:
            Last = GImg
            continue

        if (Height == 0 or Width == 0):
            Height, Width = GImg.shape
            Prev = getFixedPoints(Height, Width)
            client.send( OSCMessage("/config", ((Height, Width), Span, MinThreshold, MaxThreshold)) )
            verbosePrint(Height, Width)

        Vec = []
        Next = cv2.calcOpticalFlowPyrLK(Last, GImg, Prev, None, **LkParam)[0]
        for I in range(len(Next)):
            Pt1 = (Prev[I, 0, 0], Prev[I, 0, 1])
            Pt2 = (Next[I, 0, 0], Next[I, 0, 1])

            Dist = distance(Pt1, Pt2)
            if (Dist > MinThreshold and Dist < MaxThreshold):
                Vec.append((Pt1, Dist, getAngle(Pt1, Pt2)))
            
            if ColorState:
                cv2.circle(Img, Pt1, int(Dist), color=getDistColor(Dist))
            else:
                cv2.line(Img, Pt1, Pt2, color=(255, 255, 255))

        if (len(Vec) > 0):
            thread.start_new_thread( sendData, ("/payload", Vec) )

        if FpsState:
            end = time.time()
            img2 = cv2.flip(Img, 1)
            cv2.putText(img2, "FPS: " + str(calculateFPS(start, end)), (10,20), font, 0.5, (255, 255, 255), 2)
            start = end
            cv2.imshow('Camera', img2)
        else:
            cv2.imshow('Camera', Img[:, :: -1])
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        if k == ord('f'):
            FpsState = not FpsState
        if k == ord('c'):
            ColorState = not ColorState

        Last = GImg[:, :]


client.send( OSCMessage("/quit") )
cv2.destroyAllWindows()
Camera.release()
