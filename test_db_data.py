import os 
import numpy as np
import pandas as pd
from controllers import facial_controller , databaseController
from abc import ABC, abstractmethod
#main code 
class DatabaseFiller(ABC):
    def __init__(self):
        self.student_table = databaseController.StudentTable()
        self.class_table = databaseController.ClassTable()
        self.attendance_table = databaseController.AttendanceTable()
        self.face_table = databaseController.FaceTable()
    
    @abstractmethod
    def fill_table(self):
        pass
    
    @abstractmethod
    def read_table(self):
        pass
    
    @abstractmethod
    def delete_table(self):
        pass
    
    @abstractmethod
    def update_table(self):
        pass
    
        
    
class ClassTest(DatabaseFiller):
    def fill_table(self):
        if self.class_table.read().empty == False:
            self.delete_table()
            # class that creates class table filler data
            name = 'U.S. History'; room_number = 201; description = 'History'; start_date = '2024-01-01'; end_date = '2024-06-01'; time = '09:00:00'
            self.class_table.create(name, room_number, description, start_date, end_date, time)
            self.class_table.create('Math 101', 101, 'Introduction to Mathematics', '2022-01-01', '2022-05-01', '09:00:00')
            self.class_table.create('Physics 202', 202, 'Advanced Physics', '2024-02-01', '2024-07-01', '10:00:00')
            self.class_table.create('Chemistry 101', 203, 'Basic Chemistry', '2024-03-01', '2024-08-01', '11:00:00')
            self.class_table.create('Biology 101', 204, 'Introduction to Biology', '2024-04-01', '2024-09-01', '12:00:00')        
    
    def read_table(self):
        return self.class_table.read()
    
    def delete_table(self):
        return self.class_table.delete_all()
    
    def update_table(self):
        return self.class_table.update(1, 'U.S. History', 205, 'History', '2024-01-01', '2024-06-01', '09:00:00')
            
class StudentTest(DatabaseFiller):
    
    def test_database(self):
        if self.student_table.read().empty == False:
            self.delete_table()
            print("Student table reset for ruben")
            
        ruben = facial_controller.FacialController().process_image('./database/tests/ruben2.jpg')
        
        test_student = {'name': 'Ruben Reyes', 'classes': '[]', 'face_encoding': ruben.tolist()}
        print(ruben)
        self.student_table.create(11,test_student['name'],test_student['classes'],test_student['face_encoding'])
        print("ruben test added")
        
    def fill_table(self):
        # if self.student_table.read().size == 1:    
            picture_encoding = facial_controller.FacialController().process_image('./database/tests/Musk3.jpg')
            test_student = {'name': 'Elon Musk', 'classes': '[]', 'face_encoding': picture_encoding.tolist()}
            self.student_table.create(12,test_student['name'],test_student['classes'],test_student['face_encoding'])
            
            picture_encoding_2 = facial_controller.FacialController().process_image('./database/tests/girlTest.jpg')
            test_student_2 = {'name': 'Alice Johnson', 'classes': '[]', 'face_encoding': picture_encoding_2.tolist()}
            self.student_table.create(13,test_student_2['name'], test_student_2['classes'], test_student_2['face_encoding'])

            # picture_encoding_3 = facial_controller.FacialController().process_image('./database/tests/MaleStudentPortrait.jpg')
            # test_student_3 = {'name': 'Bob Smith', 'classes': '[]', 'face_encoding': picture_encoding_3.tolist()}
            # self.student_table.create(14,test_student_3['name'], test_student_3['classes'], test_student_3['face_encoding'])

            picture_encoding_4 = facial_controller.FacialController().process_image('./database/tests/CharlieBrownPortraitTest.jpg')
            test_student_4 = {'name': 'Charlie Brown', 'classes': '[]', 'face_encoding': picture_encoding_4.tolist()}
            self.student_table.create(15,test_student_4['name'], test_student_4['classes'], test_student_4['face_encoding'])
        # else:
            # print("Student table already has data.")
    
    def read_table(self):
        return self.student_table.read()
    
    def delete_table(self):
        return self.student_table.delete_all()
    
    def update_table(self):
        return self.student_table.update(1, 'Ruben Reyes', '[]', facial_controller.FacialController().process_image('./database/tests/ruben2.jpg'))
        
class AttendanceTest(DatabaseFiller):
    def fill_table(self):
        test_attendance = {'student_id': '1', 'class_id': '1', 'date': '2021-09-09'}
        self.attendance_table.create(test_attendance['student_id'], test_attendance['class_id'], test_attendance['date'])
        print(self.attendance_table.read())


 

    


def main() -> None:
    
    # class table filler data
    class_table = ClassTest()
    class_table.fill_table()
    # class_table.update_table()
    print(class_table.read_table())
    
    # student table filler data
    # need to run these two together
    # test_db_ruben = StudentTest()
    # test_db_ruben.test_database()
    # student = StudentTest()
    # student.fill_table()
    # student.read_table()
    
    # attendance table filler data
    # attendance = AttendanceTest()
    # attendance.fill_table()
    
    

if __name__ == '__main__':
    main()