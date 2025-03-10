import unittest
import os


from controllers import facial_controller, databaseController



class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.db_name = './database/school.db'  # Use an in-memory database for testing
        self.class_table = databaseController.ClassTable(self.db_name)
        self.student_table = databaseController.StudentTable(self.db_name)
        print(os.getcwd())

    # conditional tests
    
    
    def test_student_blank_id(self) -> None:
        self.assertIsNotNone(self.student_table.read(), None)

    def test_student_id_valid(self) -> None:
        self.assertIsNotNone(self.student_table.read(11), None)

    def test_student_id_invalid(self) -> None:
        with self.assertRaises(ValueError):
            self.student_table.read(100)

    def test_student_id_negative(self) -> None:
        with self.assertRaises(ValueError):
            self.student_table.read(-1)


    def tearDown(self):
        self.class_table.close