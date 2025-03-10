import unittest
import os
import sys
import pandas as pd
import json
from pathlib import Path

# Add the parent directory to path to import the controllers
sys.path.append(str(Path(__file__).parent.parent))
from controllers.databaseController import StudentTable

class StudentTableReadBasisPathTest(unittest.TestCase):
    def setUp(self):
        """Set up test database and populate it with test data."""
        self.db_name = ':memory:'  # Use in-memory database for testing
        self.student_table = StudentTable(self.db_name)
        
        # Add test students
        self.student_table.create("Test Student 1", 1, [1.0, 2.0, 3.0])
        self.student_table.create("Test Student 2", 2, [4.0, 5.0, 6.0])
    
    def test_path1_valid_id_record_exists(self):
        """Path 1: student_id > 0, record exists
        if student_id and student_id > 0: -> True
        if not df.empty: -> True
        """
        # Get ID of first student
        df_all = self.student_table.read_all()
        first_student_id = df_all.iloc[0]['id']
        
        df = self.student_table.read(first_student_id)
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]['id'], first_student_id)
        # Verify face_encodings was processed by json.loads
        self.assertIsInstance(df.iloc[0]['face_encodings'], list)
    
    def test_path2_valid_id_record_not_exists(self):
        """Path 2: student_id > 0, record does not exist
        if student_id and student_id > 0: -> True
        if not df.empty: -> False
        """
        # Use an ID that doesn't exist
        nonexistent_id = 999
        
        with self.assertRaises(ValueError) as context:
            self.student_table.read(nonexistent_id)
        self.assertTrue(f"No student found with ID {nonexistent_id}" in str(context.exception))
    
    def test_path3_id_is_none(self):
        """Path 3: student_id is None
        if student_id and student_id > 0: -> False
        elif student_id is None: -> True
        if not df.empty: -> True (assuming table has records)
        """
        df = self.student_table.read(None)
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 2)  # Should have 2 records
        # Verify face_encodings was processed by json.loads
        self.assertIsInstance(df.iloc[0]['face_encodings'], list)
    
    def test_path4_id_is_none_empty_table(self):
        """Path 4: student_id is None, table is empty
        if student_id and student_id > 0: -> False
        elif student_id is None: -> True
        if not df.empty: -> False
        """
        # First delete all students
        for row in self.student_table.read_all().itertuples():
            self.student_table.delete(row.id)
        
        # Now read with None ID
        df = self.student_table.read(None)
        self.assertTrue(df.empty)
    
    def test_path5_id_is_invalid(self):
        """Path 5: student_id is invalid (negative or zero)
        if student_id and student_id > 0: -> False
        elif student_id is None: -> False
        else: -> True (raise ValueError)
        """
        with self.assertRaises(ValueError) as context:
            self.student_table.read(-1)
        self.assertTrue("Invalid student ID" in str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            self.student_table.read(0)
        self.assertTrue("Invalid student ID" in str(context.exception))

    def tearDown(self):
        """Clean up after tests."""
        self.student_table.close()

if __name__ == '__main__':
    unittest.main()