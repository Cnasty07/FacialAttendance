import os 
from controllers import facial_controller , databaseController
#main code 
class DatabaseFiller:
    def __init__(self):
        self.student_table = databaseController.StudentTable()
        self.class_table = databaseController.ClassTable()
        self.attendance_table = databaseController.AttendanceTable()
        self.face_table = databaseController.FaceTable()
    
    def fill_student_table(self):
        picture_encoding = facial_controller.FacialController().process_image('./database/tests/Musk2.jpg')
        test_student = {'name': 'Elon Musk', 'classes': '[]', 'face_encoding': picture_encoding.tolist()}
        self.student_table.create(test_student['name'],test_student['classes'],test_student['face_encoding'])
        print(self.student_table.read())
    
    def fill_class_table(self):
        test_class = {'name': 'Math 101'}
        self.class_table.create(test_class['name'])
        print(self.class_table.read())
    
    def fill_attendance_table(self):
        test_attendance = {'student_id': '1', 'class_id': '1', 'date': '2021-09-09'}
        self.attendance_table.create(test_attendance['student_id'], test_attendance['class_id'], test_attendance['date'])
        print(self.attendance_table.read())
    
    



def test_database():
    # # class_table = databaseController.ClassTable().read(1)
    
    # student_table = databaseController.StudentTable()
    # ruben = facial_controller.FacialController().process_image('./database/tests/ruben2.jpg')
    
    # test_student = {'name': 'Ruben Reyes', 'classes': '1', 'face_encoding': ruben.tolist()}
    # print(ruben)
    # # student_table.update(11, test_student['name'], test_student['classes'], test_student['face_encoding'])
    # # student_table.create(test_student['name'],test_student['classes'],test_student['face_encoding'])
    # # print(class_table)
    # print(student_table.read())
    pass
    


def main() -> None:
    pass

if __name__ == '__main__':
    main()