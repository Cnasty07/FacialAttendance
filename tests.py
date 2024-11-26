import os
import controllers
import components
import database
import face_recognition
import ui
from controllers import facial_controller , databaseController

import json
import numpy as np

def add_database_entry(table_name, entry_data):
    if table_name == 'student':
        databaseController.StudentTable().create(entry_data)
    elif table_name == 'class':
        databaseController.ClassTable().create(entry_data)
    else:
        print("Invalid table name")


def test_database():
    # class_table = databaseController.ClassTable().read(1)
    
    student_table = databaseController.StudentTable()
    ruben = facial_controller.FacialController().process_image('./database/tests/ruben2.jpg')
    
    test_student = {'name': 'Ruben Reyes', 'classes': '1', 'face_encoding': ruben.tolist()}
    print(ruben)
    # student_table.update(11, test_student['name'], test_student['classes'], test_student['face_encoding'])
    # student_table.create(test_student['name'],test_student['classes'],test_student['face_encoding'])
    # print(class_table)
    print(student_table.read())


def test_facial():
    # gets image and process to encoding
    capture_test = facial_controller.FacialController().process_image('./database/tests/ruben1.jpg')

    # loads images and tests to array
    load_encoding = facial_controller.FacialController().load_known_faces()
    print(load_encoding.shape)
    # converts array to encoding

    
    print("capture: ",capture_test, "\nload: ",load_encoding)

    
    result = facial_controller.FacialController.match_processed_image(capture_test,load_encoding)
    print(result[0])

def main():
    # test_database()
    test_facial()

    # student_table = databaseController.StudentTable()
    # student_table.create('Ruben Reyes', '1', facial_controller.FacialController().process_image('./database/tests/ruben2.jpg'))
    # all_students = student_table.read()

    # # student_table.delete_all()
    # print(student_table.read())

if __name__ == '__main__':
    main() 
