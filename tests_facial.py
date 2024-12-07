import os
import json
import numpy as np
import pandas as pd
from controllers import facial_controller, databaseController

class TestFacialSystem:
    def __init__(self):
        self.fc = facial_controller.FacialController()

    def load_faces_test(self):
        lkf = self.fc.load_known_faces()
        return lkf
        
    def test_facial(self):
        # gets image and process to encoding
        unknown_face = facial_controller.FacialController().process_image('./database/tests/ruben1.jpg')
        # unknown_face = facial_controller.FacialController().process_image('./database/tests/Musk3.jpg')
        
        # loads images and tests to array
        load_known_faces = self.load_faces_test()
        # collects only the face encodings
        known_encodings = [face_encoding for face_encoding in load_known_faces]
        # Compare the unknown face to the known faces
        is_match = self.fc.match_processed_image(unknown_face, known_encodings)
        if is_match:
            print("Match found!")
        
        print(load_known_faces.index[is_match.index(True)])
        try:
            matched_student = load_known_faces.index[is_match.index(True)]
            return matched_student
        except ValueError:
            return "No match found."
        
        # result = facial_controller.FacialController.match_processed_image(capture_test,load_encoding)
        # print(result[0])
        pass



def main():
    test = TestFacialSystem()
    print(test.load_faces_test())
    match_test = test.test_facial()
    # student_table = databaseController.StudentTable()
    # student_table.create('Ruben Reyes', '1', facial_controller.FacialController().process_image('./database/tests/ruben2.jpg'))
    # all_students = student_table.read()

    # # student_table.delete_all()
    # print(student_table.read())

if __name__ == '__main__':
    main() 
