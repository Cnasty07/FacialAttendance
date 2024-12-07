import os
import face_recognition
import dlib
import numpy as np
import pandas as pd

from controllers.databaseController import ClassTable

print(os.path.dirname(os.path.relpath(__file__)))

# INFO: This class is used to compare faces to known faces in the database.

class FacialComparison:
    
    @staticmethod
    def compare_faces(known_faces_encodings:np.ndarray,new_img_encodings: np.ndarray = None) -> dict:
        """_summary_
        Checks database for a match of the new image. If found returns the student_id and the result of the comparison.
        If not found returns None.
        Args:
            new_img (np.ndarray, optional): _description_. Defaults to None.
        Returns:
            dict: array of bools to see who it is in the database
        """
        # print("known faces: ",known_faces_encodings)
        # print(type(known_faces_encodings))
        
        # image comparison to see if the image is the same person in database
        # params : known_faces_encodings, new_img_encodings in that order
        comparison = face_recognition.compare_faces(known_faces_encodings, new_img_encodings)
                
        return comparison
    
    @staticmethod
    def comparison_accuracy(student_facial_imgs = None,new_img: np.ndarray = None) -> np.linalg.norm :
        # accuracy of prediction
        face_distance = face_recognition.face_distance([student_facial_imgs], new_img)
        return face_distance
    
    
def main():
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    if dlib.DLIB_USE_CUDA:
        print("Using CUDA for dlib.")
    else:
        print("CUDA is not available for dlib.")
    new_comparison = FacialComparison()
    new_comparison.compare_faces()

if __name__ == '__main__':
    main() 
