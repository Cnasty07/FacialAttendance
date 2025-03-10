import unittest
import sqlite3
from database.recordsController import ClassTable
from radon.complexity import cc_visit

# filepath: c:\Users\chris\OneDrive\Documents\Coding_projs\Fall_2024\Programming_Langauges_Class\FacialAttendance\database\test_recordsController.py

class TestClassTable(unittest.TestCase):
    def setUp(self):
        self.db_name = ':memory:'  # Use an in-memory database for testing
        self.class_table = ClassTable(self.db_name)
        self.class_table.create("Math 101", 101, "Introductory Math", "2024-01-15", "2024-05-15", "09:00:00")

    def tearDown(self):
        self.class_table.close()

    def test_read(self):
        # Test reading an existing class record
        class_record = self.class_table.read(1)
        self.assertIsNotNone(class_record)
        self.assertEqual(class_record[1], "Math 101")
        self.assertEqual(class_record[2], 101)
        self.assertEqual(class_record[3], "Introductory Math")

        # Test reading a non-existing class record
        class_record = self.class_table.read(999)
        self.assertIsNone(class_record)

    def test_cyclomatic_complexity_read(self):
        with open('recordsController.py', 'r') as file:
            code = file.read()
        complexity = cc_visit(code)
        read_function_complexity = next((c for c in complexity if c.name == 'read' and c.classname == 'ClassTable'), None)
        self.assertIsNotNone(read_function_complexity)
        self.assertEqual(read_function_complexity.complexity, 1)  # Expected cyclomatic complexity is 1

if __name__ == '__main__':
    unittest.main()