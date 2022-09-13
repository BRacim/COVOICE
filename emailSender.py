
# envoie de mail ...
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import imghdr
import smtplib
import os


class EmailSender(object):
    def __init__(self, recepteurEmail, qrCodeName):
        self.bodyMessage = "Bonjour :) \nCi joint votre Code QR généré.\nVeuillez le présenter à notre interphone.Merci.\nCordialement.\nCovoice-Team"
        self.fileName = qrCodeName
        self.covoiceEmail = "interphone.covoice@gmail.com"  # covoice.compagnie@gmail.com
        self.covoiceEmailPassword = "TheCovoice"  # 123456789RYP
        self.subject = "Covoice-Validation du code QR-"
        self.recepteurEmail = recepteurEmail

    def sendMail(self):
        msg = MIMEMultipart()
        msg['From'] = self.covoiceEmail
        msg['To'] = self.recepteurEmail
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.bodyMessage, 'plain'))
        attachment = open(self.fileName, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= "+self.fileName)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.covoiceEmail, self.covoiceEmailPassword)

        server.sendmail(self.covoiceEmail, self.recepteurEmail, text)
        server.quit()


# myEmail = EmailSender("nacimessi10@outlook.fr", "nassim")
# myEmail.sendMail()
