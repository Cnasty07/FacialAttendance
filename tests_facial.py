import os
import json
import numpy as np
import pandas as pd
from controllers import facial_controller, databaseController

def test_facial():
    # gets image and process to encoding
    # capture_test = facial_controller.FacialController().process_image('./database/tests/ruben1.jpg')

    # loads images and tests to array
    load_encoding = facial_controller.FacialController().load_known_faces()
    # print(load_encoding.shape)
    # converts array to encoding
    
    # print("capture: ",capture_test, "\nload: ",load_encoding)

    
    # result = facial_controller.FacialController.match_processed_image(capture_test,load_encoding)
    # print(result[0])
    pass



def main():
    # test_database()
    # new_db_test = TestDatabase()
    # new_db_test.test_student_table()
    
    
    
    test_facial()

    # student_table = databaseController.StudentTable()
    # student_table.create('Ruben Reyes', '1', facial_controller.FacialController().process_image('./database/tests/ruben2.jpg'))
    # all_students = student_table.read()

    # # student_table.delete_all()
    # print(student_table.read())

if __name__ == '__main__':
    main() 
