from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import imghdr
import smtplib
import os
import sqlite3


class CovoiceDB(object):
    def __init__(self, bdd):
        self.connection = sqlite3.connect(bdd)
        self.cursor = None
        self.tuple = None
        self.user = None
        self.userList = []

    def initCursor(self,):
        self.cursor = self.connection.cursor()

    def setTuple(self, first_name, last_name, age, email, statut, voicePin):  # statut = 1->v 2-> r 3->f

        self.tuple = (self.cursor.lastrowid, first_name, last_name, age, email, str(
            first_name)+"_"+str(last_name)+".jpg", statut, voicePin, "qr_"+str(
            first_name)+"_"+str(last_name)+".png")

    def insertNewUser(self):
        self.cursor.execute(
            "INSERT INTO User(id,first_name, last_name, age, email,image,userStatutCovoice,voicePin,qrCode ) values(?,?,?,?,?,?,?,?,?)", self.tuple)
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()

    def getAllResident(self):
        self.cursor.execute(f"SELECT * FROM User WHERE userStatutCovoice = '2' ")
        self.userList = list(self.cursor.fetchall())
        print(self.userList)

    def existeInDataBase(self, qrData):
        self.cursor.execute(f"SELECT * FROM User WHERE qrCode='{qrData}'")
        toto = list(self.cursor.fetchall())
        print(len(toto))
        if len(toto) > 0:
            return True
        else:
            return False


# covoiceRequest = CovoiceDB("covoiceUsers.db")
# covoiceRequest.initCursor()
# # covoiceRequest.setTuple("Racim", "boumbar", 25, "racimboumbar@gmail.fr", 2, 16)
# # covoiceRequest.insertNewUser()
# # covoiceRequest.initCursor()
# # covoiceRequest.setTuple("Yann", "Yann", 25, "YannYann@gmail.fr", 2, 26)
# # covoiceRequest.insertNewUser()
# # covoiceRequest.closeConnection()
# covoiceRequest.getAllUsers()
