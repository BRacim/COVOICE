import face_recognition
import picamera
import numpy as np


class FaceCamera(object):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.output = None

    def initCamera(self):
        self.camera.resolution = (320, 240)
        self.output = np.empty((240, 320, 3), dtype=np.uint8)

    def initFaceRecognition(self, param):
        user_image = face_recognition.load_image_file(param)
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        return user_face_encoding
