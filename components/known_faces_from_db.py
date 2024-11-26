import os
import cv2
import face_recognition
import numpy as np
import sqlite3
import pandas as pd
import controllers.databaseController as db



# TODO: get tables from db to add to known faces
#       1. class specific to pull students from db
#       2. get student id and face data
#       3. add to known faces


class KnownFaces:
    def __init__(self, db_path):
            self.db_path = db_path
            self.known_face_encodings = []
            self.known_face_names = []

    
    def load_known_faces(self,class_id):
        # gets class id from interface
        class_table = db.ClassTable()
        class_table.read(class_id=class_id)
        student_ids_for_class = class_table.read(class_id=class_id)

        class_table.conn.close()
        
    @staticmethod
    def get_known_faces(self):
        return self.known_face_encodings, self.known_face_names
    
    
def main():
    
    db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../database/school.db')
    known_faces = KnownFaces(db_name)
    known_faces.load_known_faces(1)

if __name__ == '__main__':
    main() 
