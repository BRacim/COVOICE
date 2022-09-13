
from threading import Thread
import face_recognition
import cv2
import picamera
import numpy as np
# import qrcode
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


class Interface(Thread):
    def __init__(self, ):
        Thread.__init__(self)
        self.userMessage = None
        self.ll = None
        self.myResidentList = None

    def run(self):
        Covoice = Tk()
        img = ImageTk.PhotoImage(Image.open("Covoice.jpg"))
        # Covoice.attributes('-fullscreen', True)

        # Covoice.bind('<Escape>', lambda e: Covoice.destroy())

        self.userMessage = tk.StringVar()
        Covoice.title("Covoice")

        Covoice.config(background='#FFCC66')

        label_text1 = Label(Covoice, text="COVOICE", font=(
            "times new roman", 20), bg='#FFCC66', fg='black')
        label_text1.grid(row=0, column=0)

        label_text = Label(Covoice, text="Bienvenue", font=(
            "times new roman", 40), bg='#FFCC66', fg='white')
        label_text.grid(row=2, column=5)

        panel = Label(Covoice, image=img)
        panel.grid(row=4, column=5)

        panelMessageUser = Label(Covoice, textvariable=self.userMessage, font=(
            "times new roman", 20), bg='#FFCC66', fg='black')
        panelMessageUser.grid(row=6, column=5, padx=(10, 100))

        self.myResidentList = tk.Listbox(Covoice, width=50)
        self.myResidentList.grid_forget()

        Covoice.mainloop()
