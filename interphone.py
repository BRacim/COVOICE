
from threading import Thread
import face_recognition
import cv2
import picamera
import numpy as np
# import qrcode
from interface import Interface

from test_QR import TestQR
from extracted import ExtractedPart
# Importation des librairies DES GPIOs
import RPi.GPIO as GPIO
from camera import FaceCamera
from DB_connection import CovoiceDB
from emailSender import EmailSender
# Set function to calculate percent from angle
import threading

import tkinter as tk
from tkinter import *
import time
from PIL import ImageTk, Image
import os
import cv2
import picamera
import numpy as np


class Interphone(Thread):
    def __init__(self, ):
        Thread.__init__(self)
        self._isConfirmed = False
        self.qrdata = None
        self.myCam = FaceCamera()
        self.stop_threads = False
        self._correspondingUser = None
        self.data = None
        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()
        self.pwm_gpio = 5
        self.frequence = 50

        self.led_vert = 13
        self.led_rouge = 6
        self.covoiceRequest = None
        self.inter = Interface()
        self.threadWaitInviter = None
        self.threadSendMail = None
        self.sendMail = True
        self.isInviterDetected = False
        self.threadQRcamera = None
        self.countdownQRverification = None
        self.listThreadInviter = []

    def waitingForQRCamera(self):
        print("Debut de la confirmation QR")
        # testQR = TestQR()
        # testQR.testQR(self.myCam.output)
        print("on est dans test_QR")
        while True:
            _, img = self.cap.read()
            self.data, bbox, _ = self.detector.detectAndDecode(img)
            if self.data or self._isConfirmed:
                break
        self.cap.release()
        cv2.destroyAllWindows()
        print("Ma data est {}".format(self.data))
        if self.data:
            print("j'ai trouvé la data")
            self.qrdata = self.data
            self.inter.userMessage.set("QR code identifié")

    def jsk(self):
        self._isConfirmed = True
        if self.threadQRcamera.isAlive():
            self.threadQRcamera.join()

    def confirmation(self):

        _waintingForConfirmationQR = threading.Timer(20.0, self.jsk)
        _waintingForConfirmationQR.start()
        _waintingForConfirmationQR.join()

    def cameraFunction(self):
        state = GPIO.input(self._correspondingUser[7])
        print(state)
        self.inter.userMessage.set(
            "parlez ...")
        while not state:
            # attendre signal vocal
            state = GPIO.input(self._correspondingUser[7])
            time.sleep(0.02)
            GPIO.output(self.led_rouge, True)
            time.sleep(0.02)
            if state:
                self.stop_threads = True
                self.sendMail = False
            if self.stop_threads:
                GPIO.output(self.led_rouge, False)
                self.threadSendMail.join()
                break

    def matoub(self):
        self.stop_threads = True
        EmailSender(
            self._correspondingUser[4], self._correspondingUser[8]).sendMail()

    def sendMailFunction(self):

        _waitAndSendMail = threading.Timer(10.0, self.matoub)
        _waitAndSendMail.start()
        _waitAndSendMail.join()

    def angle_to_percent(self, angle):
        if angle > 180 or angle < 0:
            return False

        start = 4
        end = 12.5
        ratio = (end - start)/180  # Calcul ratio from angle to percent

        angle_as_percent = angle * ratio

        return start + angle_as_percent

    def mnanauk(self):

        _waitAndSendMail = threading.Timer(15.0, self.jsk)
        _waitAndSendMail.start()
        _waitAndSendMail.join()

    def tmenyik(self, resident):
        state = GPIO.input(resident[7])
        print(resident[7])
        self.inter.userMessage.set(
            "parlez ...")
        while not state:
            # attendre signal vocal
            print("isConfirmed= {}".format(self._isConfirmed))
            print(state)
            state = GPIO.input(resident[7])
            time.sleep(0.02)
            GPIO.output(self.led_rouge, True)
            time.sleep(0.02)
            if self._isConfirmed:
                break
            if state:
                print("Oui j'ai entendu la voix")
                self.isInviterDetected = True
                self._isConfirmed = True
                # self.threadWaitInviter.join()
                break

    def detectionVocaleInviter(self):
        print("parlez ")
        self.inter.userMessage.set(
            "parlez")

        # t1 = threading.Thread(target=self.tmenyik, args=[
        #     self.covoiceRequest.userList[0]])

        # t2 = threading.Thread(target=self.tmenyik, args=[
        #     self.covoiceRequest.userList[1]])
        # t2.start()
        # t1.start()
        # t1.join()
        # t2.join()

        for _resident in self.covoiceRequest.userList:
            self.listThreadInviter.append(threading.Thread(
                 target=self.tmenyik, args=[_resident]))
        print("\nListe des thread est : {} \n".format(self.listThreadInviter))
        for _thread in self.listThreadInviter:
             _thread.start()

        for _endThread in self.listThreadInviter:
             _endThread.join()

    def run(self):
        self.inter.start()

        self.covoiceRequest = CovoiceDB("covoiceUsers.db")
        self.covoiceRequest.initCursor()
        self.covoiceRequest.getAllResident()

        self.myCam.initCamera()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_vert, GPIO.OUT, initial=False)
        GPIO.setup(self.led_rouge, GPIO.OUT, initial=False)
        _usersFaceEncoding = []
        for _user in self.covoiceRequest.userList:
            GPIO.setup(_user[7], GPIO.IN)
            _usersFaceEncoding.append(
                self.myCam.initFaceRecognition(_user[5]))

        GPIO.setup(self.pwm_gpio, GPIO.OUT)
        pwm = GPIO.PWM(self.pwm_gpio, self.frequence)

        GPIO.setwarnings(False)

        face_locations = []
        face_encodings = []
        time.sleep(1)

        while True:

            extracted = ExtractedPart()
            zebi = extracted.traitement(
                self.myCam.camera, self.myCam.output, face_encodings)
            for face_encoding in zebi:
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces(
                    _usersFaceEncoding, face_encoding)
                self.inter.userMessage.set(
                    "recherche d'une personne")
                if True in match:
                    # get user:
                    self._correspondingUser = self.covoiceRequest.userList[match.index(
                        True)]
                    self.inter.userMessage.set("Bonjour {} {}".format(
                        self._correspondingUser[1], self._correspondingUser[2]))
                    print("I see someone named {} {}!".format(
                        self._correspondingUser[1], self._correspondingUser[2]))
                    # Timer 60s
                    # à la fin des 60 secondes
                    # email

                    t3 = threading.Thread(target=self.cameraFunction)
                    t3.start()
                    self.threadSendMail = threading.Thread(
                        target=self.sendMailFunction)
                    self.threadSendMail.start()
                    t3.join()
                    if self.threadSendMail.isAlive():
                        self.threadSendMail.join()
                    if not self.sendMail:  # ouverture de la porte
                        self.inter.userMessage.set(
                            "Ouverture de la porte ...")
                        GPIO.output(self.led_vert, True)
                        pwm.start(self.angle_to_percent(0))
                        time.sleep(1)
                        pwm.ChangeDutyCycle(self.angle_to_percent(90))
                        time.sleep(5)
                        GPIO.output(self.led_vert, False)
                        pwm.ChangeDutyCycle(self.angle_to_percent(0))
                        time.sleep(1)
                        pwm.stop()
                    else:  # envoie de mail
                        self.inter.userMessage.set(
                            "Vérification du QR en cours ...")

                        self.myCam.camera.close()
                        self._isConfirmed = False
                        self.threadQRcamera = threading.Thread(
                            target=self.waitingForQRCamera)
                        self.threadQRcamera.start()
                        self.countdownQRverification = threading.Thread(
                            target=self.confirmation)
                        self.countdownQRverification.start()
                        self.threadQRcamera.join()
                        self.countdownQRverification.join()
                        self.myCam = FaceCamera()
                        self.myCam.initCamera()
                        if not self.qrdata:
                            continue
                        else:

                            if self.qrdata == self._correspondingUser[8][0: len(self._correspondingUser[8]) - 4]:
                                self.inter.userMessage.set(
                                    "Bienvenue {} {} \nOuverture de la porte...".format(self._correspondingUser[1], self._correspondingUser[2]))
                                GPIO.output(self.led_vert, True)
                                pwm.start(self.angle_to_percent(0))
                                time.sleep(1)
                                pwm.ChangeDutyCycle(self.angle_to_percent(90))
                                time.sleep(5)
                                GPIO.output(self.led_vert, False)
                                pwm.ChangeDutyCycle(self.angle_to_percent(0))
                                time.sleep(1)
                                pwm.stop()

                            else:
                                continue

                else:
                    self.inter.userMessage.set("Introduissez votre QRcode")
                    self.myCam.camera.close()
                    self._isConfirmed = False
                    self.threadQRcamera = threading.Thread(
                        target=self.waitingForQRCamera)
                    self.threadQRcamera.start()
                    self.countdownQRverification = threading.Thread(
                        target=self.confirmation)
                    self.countdownQRverification.start()
                    if self.threadQRcamera.isAlive():
                        self.threadQRcamera.join()
                    if self.countdownQRverification.isAlive():
                        self.countdownQRverification.join()
                    self.myCam = FaceCamera()
                    self.myCam.initCamera()
                    if self.qrdata is not None:
                        if self.covoiceRequest.existeInDataBase(str(self.qrdata) + ".png"):
                            self.inter.userMessage.set(
                                "ouverture de porte du facteur")
                            GPIO.output(self.led_vert, True)
                            pwm.start(self.angle_to_percent(0))
                            time.sleep(1)
                            pwm.ChangeDutyCycle(self.angle_to_percent(90))
                            time.sleep(5)
                            GPIO.output(self.led_vert, False)
                            pwm.ChangeDutyCycle(self.angle_to_percent(0))
                            time.sleep(1)
                            pwm.stop()
                        else:
                            self.inter.userMessage.set("QR code invalide")
                            GPIO.output(self.led_rouge, True)
                            time.sleep(1)
                            GPIO.output(self.led_rouge, False)
                    else:
                        print("processus actuel des interphones")
                        self.inter.userMessage.set(
                            "liste des habitants")
                        for _resident in self.covoiceRequest.userList:
                            self.inter.myResidentList.insert(
                                tk.END, "{} - {}".format(_resident[1], _resident[2]))
                        print("avant l'affichage grid")
                        self.inter.myResidentList.grid(row=8, column=5)
                        print("aprés affichage grid")
                        self._isConfirmed = False
                        _t3 = threading.Thread(
                            target=self.detectionVocaleInviter)
                        _t3.start()
                        self.threadWaitInviter = threading.Thread(
                            target=self.mnanauk)
                        self.threadWaitInviter.start()
                        _t3.join()
                        print(self.threadWaitInviter.isAlive())
                        if self.threadWaitInviter.isAlive():
                            self.threadWaitInviter.join()

                        if self.isInviterDetected:
                            self.inter.userMessage.set(
                                "Ouverture de la porte ...")
                            GPIO.output(self.led_vert, True)
                            pwm.start(self.angle_to_percent(0))
                            pwm.ChangeDutyCycle(self.angle_to_percent(90))
                            time.sleep(5)
                            GPIO.output(self.led_vert, False)
                            pwm.ChangeDutyCycle(self.angle_to_percent(0))
                            time.sleep(1)
                            pwm.stop()

                        else:
                            continue

        self.inter.join()
