from decimal import DivisionByZero
import cv2
from cv2 import threshold
import numpy as np
import dlib
from math import hypot
import time

import pathlib
import os
from tkinter import Image
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import glob
import face_recognition
class ImageThread(QThread):
    imageUpdate = pyqtSignal(QImage)
    path = glob.glob("/profileImage/*.jpg")
    datFile = r"C:\Users\Admin\Documents\shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(datFile)
    start_time = time.time()
    note = False
    def run(self):
        self.cascade_classifier = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
        self.threadActive = True
        self.pressCheck = False
        self.faceCheck = False
        self.classFoundName = ''
        Capture = cv2.VideoCapture(0)
        while self.threadActive:
            ret, frame = Capture.read()
            gray = cv2.cvtColor(frame, 0)
            detections = self.cascade_classifier.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
            if(len(detections) > 0):
                (x,y,w,h) = detections[0]
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            if self.pressCheck:
                self.pressCheck = False
                img_name = 'image/tmp.jpg'
                cv2.imwrite(img_name,frame)
                self.faceCompare()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flippedImage = cv2.flip(image, 1)
                ConvertToQtFormat = QImage(flippedImage.data, flippedImage.shape[1], flippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 500, Qt.KeepAspectRatio)
                self.imageUpdate.emit(Pic)
        Capture.release()
#=========================================
    def get_blinking_ratio(self,eyes_points, facial_landmarks):
        left_point = (facial_landmarks.part(
            eyes_points[0]).x, facial_landmarks.part(eyes_points[0]).y)
        right_point = (facial_landmarks.part(
            eyes_points[3]).x, facial_landmarks.part(eyes_points[3]).y)
        center_top = self.midpoint(facial_landmarks.part(
            eyes_points[1]), facial_landmarks.part(eyes_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(
            eyes_points[5]), facial_landmarks.part(eyes_points[4]))

        hot_line_length = hypot(
            (left_point[0]-right_point[0]), (left_point[1]-right_point[1]))
        ver_line_length = hypot(
            (center_top[0]-center_bottom[0]), (center_top[1]-center_bottom[1]))

        ratio = hot_line_length / ver_line_length
        return ratio
    def midpoint(self,p1, p2):
        return int((p1.x+p2.x)/2), int((p1.y + p2.y)/2)
    def blink(self,frame):
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray1)
        for face in faces:
            landmarks = self.predictor(gray1, face)
            left_eye_ratio = self.get_blinking_ratio(
                [36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = self.get_blinking_ratio(
                [42, 43, 44, 45, 46, 47], landmarks)
            try:
                blinking_ratio = (right_eye_ratio+left_eye_ratio)/2
            except DivisionByZero:
                blinking_ratio = 0
            if blinking_ratio > 4.0:
                end_time = time.time()
                t = end_time-self.start_time
                if(t > 5):
                    self.note = True
            else:
                self.start_time = time.time()
                self.note = False
#=========================================

    def stop(self):
        self.threadActive = False
        self.quit()
    
    
    def faceCompare(self):
        img1 = face_recognition.load_image_file("image/tmp.jpg")
        img1_encode = face_recognition.face_encodings(img1)
        boolCheck = False
        if len(img1_encode) == 0:
            self.faceCheck = False
            return
        else:
            self.faceCheck = True
        img1_encode = img1_encode[0]
        path = os.listdir("profileImage")
        for img in path:
            img2 = cv2.imread(f'profileImage/{img}')
            img2_encode = face_recognition.face_encodings(img2)
            if len(img2_encode) == 0:
                continue
            img2_encode = img2_encode[0]
            results = face_recognition.compare_faces([img1_encode], img2_encode)    
            faceDistance = face_recognition.face_distance([img1_encode],img2_encode)
            if(results[0] == True and faceDistance[0] <= 0.4): 
                boolCheck = True
                self.classFoundName = img[0:len(img)-4]
                print("Found")
                break
        if(boolCheck == False):
            self.classFoundName = "None"
        return boolCheck        

