import face_recognition


class ExtractedPart():
   
    def traitement(self, camera, output,face_encodings):
        print("Capturing image.")
        camera.capture(output, format="rgb")
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(
            output, face_locations)
        return face_encodings        
