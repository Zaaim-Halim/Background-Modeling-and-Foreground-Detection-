# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 12:23:17 2021

@author: zaaim halim - master midvi
"""
import numpy as np
import cv2
import  sys



class BackgroundSubstractionALGO:
    def __init__(self):
        self.frames = []
        self.isframesfull = False

    def frame_differencing(self,frame,modelPath,threshold):
        foreground = cv2.absdiff(self.fixed_backgroundModel(modelPath) , cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
        th , foreground = cv2.threshold(foreground,threshold, 255, cv2.THRESH_BINARY)

        cv2.namedWindow("Channels")
        cv2.imshow("Channelas", foreground)


    def mean_filter(self,frame,threshold,numFrame):
       #frame =  cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
       if not self.isframesfull:
           self.frames.append(frame)

       if len(self.frames) == numFrame:
           median_model = np.mean(self.frames, axis=0).astype(dtype=np.uint8)
           foreground = cv2.absdiff(median_model,frame).astype(np.uint8)
           th , foreground = cv2.threshold(foreground, threshold, 255, cv2.THRESH_BINARY)
           cv2.namedWindow("Channels")
           cv2.imshow("Channels",foreground)
           self.isframesfull = True


    def median_filter(self,frame,threshold,numFrame):

      # frame =  cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
       if not self.isframesfull:
           self.frames.append(frame)

       if len(self.frames) == numFrame:
           median_model = np.median(self.frames, axis=0).astype(dtype=np.uint8)
           foreground = cv2.absdiff(median_model,frame).astype(np.uint8)
           th , foreground = cv2.threshold(foreground, threshold, 255, cv2.THRESH_BINARY)
           cv2.namedWindow("Channels")
           cv2.imshow("Channels",foreground)
           self.isframesfull = True


    def running_average(self,frame,threshold,numFrame,alpha=.7):
       # frame =  cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
       # frames list is intended to hold just one element at each call ##
       if not self.isframesfull:
           self.frames.append(frame)

       if len(self.frames) == numFrame:
          model = cv2.addWeighted(self.frames[0],(1-alpha),frame,alpha,0)
          foreground = cv2.absdiff(model,frame)
          th , foreground = cv2.threshold(foreground, threshold, 255, cv2.THRESH_BINARY)
          cv2.namedWindow("Channels")
          cv2.imshow("Channels",foreground)
          self.frames.pop()
          self.frames.append(model)
          self.isframesfull = True

    def fixed_backgroundModel(self,path):
        model = cv2.imread(path)
        model = cv2.resize(model,(600,450))
        return cv2.cvtColor(model, cv2.COLOR_BGR2GRAY)

    def initframes(self):
        self.frames.clear()


def decideOperation(algorithm,operation,currentFrame,threshold,numFrame):
    if operation == "Frame_differencing":
        algorithm.frame_differencing(currentFrame,"me.JPG",threshold)
    elif operation == "Mean_filter":
        algorithm.mean_filter(currentFrame,threshold,numFrame)

    elif operation == "Median_filter":
        algorithm.median_filter(currentFrame,threshold, numFrame)

    elif operation == "Running_average":
        algorithm.running_average(currentFrame,threshold,numFrame)
    else:

        print("Operation not supported !")



class ReadVideo:
    def __init__(self,path=None,isFromWebCam=False):
        self.path = path
        self.cap = ""
        self.isFromWebCam = isFromWebCam
        self.threshold = 10
        self.numFrame = 15
        self.algorithm = BackgroundSubstractionALGO()

    def load(self):
        if not self.isFromWebCam:
           self.cap = cv2.VideoCapture(self.path)
        else:
            self.cap = cv2.VideoCapture(0)

    def capture(self,operation):
        if(self.cap.isOpened() == False):
            print("Error opening video stream or file")
            sys.exit(0)
        while (self.cap.isOpened()):
            ret , currentFrame = self.cap.read()

            if ret:
                currentFrame = cv2.resize(currentFrame,(600,450))
                decideOperation(self.algorithm,operation,currentFrame,self.threshold,
                                self.numFrame)
                cv2.namedWindow("Main")
                cv2.imshow("Main", currentFrame)
                if cv2.waitKey(25) & 0XFF ==  ord('q'):
                    break
            else:
                print('no video')
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.release()
        self.cleanup()


    def release(self):
        self.cap.release()

    def cleanup(self):
        cv2.destroyAllWindows()

    def set_isFromWebCam(self,boolean):
        self.isFromWebCam = boolean

    def set_path(self,p):
        self.path = p

    def set_thresh(self , thresh):
        self.threshold = thresh

    def set_numFrame(self, numf):
        self.numFrame = numf