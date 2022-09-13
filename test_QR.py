import cv2
import picamera
import numpy as np


class TestQR():
    def __init__(self):
        self.data = None
        self.cap = cv2.VideoCapture(0)
        self.detector = cv2.QRCodeDetector()

    def testQR(self, output):
        """test le qr et retourne la data dans le cas ou ça match"""
        print("on est dans test_QR")
        while True:
            _, img = self.cap.read()
            self.data, bbox, _ = self.detector.detectAndDecode(img)
            if self.data:
                break
        self.cap.release()
        cv2.destroyAllWindows()
