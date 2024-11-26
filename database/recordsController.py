import sqlite3
import json
from abc import ABC, abstractmethod


class DatabaseController(ABC):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Failed to connect to the database: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database query failed: {e}")
    
    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass



class ClassTable(DatabaseController):
    """managing the 'class' table."""
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                room_number INTEGER NOT NULL,
                                description TEXT,
                                start_date DATE,
                                end_date DATE,
                                time TIME)''')
        self.conn.commit()

    def create(self, name, room_number, description, start_date, end_date, time):
        """Create a new class record"""
        self.execute_query(
            'INSERT INTO class (name, room_number, description, start_date, end_date, time) VALUES (?, ?, ?, ?, ?, ?)',
            (name, room_number, description, start_date, end_date, time)
        )

    def read(self, class_id):
        """Read a class record by ID."""
        self.cursor.execute('SELECT * FROM class WHERE id = ?', (class_id,))
        return self.cursor.fetchone()

    def read_all(self):
        """Read all class records."""
        self.cursor.execute('SELECT * FROM class')
        return self.cursor.fetchall()

    def update(self, class_id, name, room_number, description, start_date, end_date, time):
        """Update a class record."""
        self.execute_query(
            'UPDATE class SET name = ?, room_number = ?, description = ?, start_date = ?, end_date = ?, time = ? WHERE id = ?',
            (name, room_number, description, start_date, end_date, time, class_id)
        )

    def delete(self, class_id):
        """Delete a class record."""
        self.execute_query('DELETE FROM class WHERE id = ?', (class_id,))


class StudentTable(DatabaseController):
    """Class for managing the 'student' table."""
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                classes INTEGER,
                                face_encodings TEXT,
                                FOREIGN KEY (classes) REFERENCES class(id))''')
        self.conn.commit()

    def create(self, name, classes, face_encodings):
        """Create a new student record."""
        encoding_json = json.dumps(face_encodings)
        self.execute_query(
            'INSERT INTO student (name, classes, face_encodings) VALUES (?, ?, ?)',
            (name, classes, encoding_json)
        )

    def read(self, student_id):
        """Read a student record by ID."""
        self.cursor.execute('SELECT * FROM student WHERE id = ?', (student_id,))
        row = self.cursor.fetchone()
        if row:
            row = list(row)
            row[3] = json.loads(row[3])  # Deserialize face encodings
        return row

    def read_all(self):
        """Read all student records."""
        self.cursor.execute('SELECT * FROM student')
        return self.cursor.fetchall()

    def update(self, student_id, name, classes, face_encodings):
        """Update a student record."""
        encoding_json = json.dumps(face_encodings)
        self.execute_query(
            'UPDATE student SET name = ?, classes = ?, face_encodings = ? WHERE id = ?',
            (name, classes, encoding_json, student_id)
        )

    def delete(self, student_id):
        """Delete a student record."""
        self.execute_query('DELETE FROM student WHERE id = ?', (student_id,))


class AttendanceTable(DatabaseController):
    """Class for managing the 'attendance' table."""
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                class_id INTEGER,
                                student_id INTEGER,
                                date DATE,
                                status TEXT,
                                FOREIGN KEY (class_id) REFERENCES class(id),
                                FOREIGN KEY (student_id) REFERENCES student(id))''')
        self.conn.commit()

    def create(self, class_id, student_id, date, status):
        """Create a new attendance record."""
        if status not in ["Present", "Absent"]:
            raise ValueError("Invalid status. Must be 'Present' or 'Absent'.")
        self.execute_query(
            'INSERT INTO attendance (class_id, student_id, date, status) VALUES (?, ?, ?, ?)',
            (class_id, student_id, date, status)
        )

    def read(self, attendance_id):
        """Read an attendance record by ID."""
        self.cursor.execute('SELECT * FROM attendance WHERE id = ?', (attendance_id,))
        return self.cursor.fetchone()

    def filter_by_class(self, class_id):
        """Filter attendance records by class ID."""
        self.cursor.execute('SELECT * FROM attendance WHERE class_id = ?', (class_id,))
        return self.cursor.fetchall()

    def filter_by_student(self, student_id):
        """Filter attendance records by student ID."""
        self.cursor.execute('SELECT * FROM attendance WHERE student_id = ?', (student_id,))
        return self.cursor.fetchall()

    def filter_by_date_range(self, start_date, end_date):
        """Filter attendance records by date range."""
        self.cursor.execute('SELECT * FROM attendance WHERE date BETWEEN ? AND ?', (start_date, end_date))
        return self.cursor.fetchall()

    def update(self, attendance_id, class_id, student_id, date, status):
        """Update an attendance record."""
        self.execute_query(
            'UPDATE attendance SET class_id = ?, student_id = ?, date = ?, status = ? WHERE id = ?',
            (class_id, student_id, date, status, attendance_id)
        )

    def delete(self, attendance_id):
        """Delete an attendance record."""
        self.execute_query('DELETE FROM attendance WHERE id = ?', (attendance_id,))


class FaceTable(DatabaseController):
    """Class for managing the 'face' table."""
    def __init__(self, db_name):
        super().__init__(db_name)
        self.connect()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS face (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                student_id INTEGER,
                                encoding TEXT,
                                FOREIGN KEY (student_id) REFERENCES student(id))''')
        self.conn.commit()

    def create(self, student_id, encoding):
        """Create a new face encoding record."""
        encoding_json = json.dumps(encoding)
        self.execute_query(
            'INSERT INTO face (student_id, encoding) VALUES (?, ?)',
            (student_id, encoding_json)
        )

    def read(self, face_id):
        """Read a face encoding record by ID."""
        self.cursor.execute('SELECT * FROM face WHERE id = ?', (face_id,))
        row = self.cursor.fetchone()
        if row:
            row = list(row)
            row[2] = json.loads(row[2])  # Deserialize encoding
        return row

    def find_by_student(self, student_id):
        """Find all face encodings for a student."""
        self.cursor.execute('SELECT * FROM face WHERE student_id = ?', (student_id,))
        return self.cursor.fetchall()

    def update(self, face_id, student_id, encoding):
        """Update a face encoding record."""
        encoding_json = json.dumps(encoding)
        self.execute_query(
            'UPDATE face SET student_id = ?, encoding = ? WHERE id = ?',
            (student_id, encoding_json, face_id)
        )

    def delete(self, face_id):
        """Delete a face encoding record."""
        self.execute_query('DELETE FROM face WHERE id = ?', (face_id,))


def main():
    """Main function for testing the database functionality."""
    db_name = './database/school.db'

    # Example usage
    class_table = ClassTable(db_name)
    class_table.create("Math 101", 101, "Introductory Math", "2024-01-15", "2024-05-15", "09:00:00")
    print(class_table.read_all())
    # student_table = StudentTable(db_name)
    # student_table.create("Alice Johnson", 1, ["encoding_data"])

    # attendance_table = AttendanceTable(db_name)
    # attendance_table.create(1, 1, "2024-01-16", "Present")

    # face_table = FaceTable(db_name)
    # face_table.create(1, ["face_encoding_data"])

    print("Setup complete.")


if __name__ == "__main__":
    main()
