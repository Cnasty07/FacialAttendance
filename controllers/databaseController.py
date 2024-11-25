import sqlite3
import json
from abc import ABC, abstractmethod
import os
import pandas as pd


# TODO: Change the face encoding to a numpy array
# TODO: Add a method to convert the numpy array to a string for storage in the database
# TODO: Add a method to convert the string back to a numpy array when reading from the database


class DatabaseController(ABC):
    def __init__(self, db_name: str = None):
        if db_name is None:
            db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database/school.db')
        else :
            self.db_name = db_name
        self.table_name = None
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
    def __init__(self, db_name: str = None): 
        self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database/school.db')
        super().__init__(db_name)
        self.table_name = 'class'
        self.connect()


    def create(self, name, room_number, description, start_date, end_date, time):
        """Create a new class record using pandas."""
        data = {
            'name': [name],
            'room_number': [room_number],
            'description': [description],
            'start_date': [start_date],
            'end_date': [end_date],
            'time': [time]
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def read(self, class_id=None):
        """Read a class record using pandas."""
        if class_id:
            return pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE id = {class_id}", self.conn)
        else:
            return pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)
        
    def read_all(self):
        """Read all class records using pandas."""
        return pd.read_sql_query("SELECT * FROM class", self.conn)
    
    def update(self, class_id, name, room_number, description, start_date, end_date, time):
        """Update a class record using pandas."""
        data = {
            'name': name,
            'room_number': room_number,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'time': time
        }
        df = pd.DataFrame([data])
        df.to_sql(self.table_name, self.conn, if_exists='replace', index=False, method='multi', chunksize=1000)

    def delete(self, class_id):
        """Delete a class record using pandas."""
        query = f"DELETE FROM {self.table_name} WHERE id = {class_id}"
        self.execute_query(query)
    
class StudentTable(DatabaseController):
    """Class for managing the 'student' table."""
    def __init__(self, db_name: str = None):
        self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database/school.db')
        super().__init__(db_name)
        self.table_name = 'student'
        self.connect()
        data = {
            'id': [],
            'name': [],
            'classes': [],
            'face_encodings': []
        }
        df = pd.DataFrame(data)
        try:
            df.to_sql(self.table_name, self.conn, if_exists='fail', index=False)
        except ValueError:
            print(f"Table {self.table_name} already exists.")

    def create(self, name, classes, face_encodings):
        """Create a new student record using pandas."""
        encoding_json = json.dumps(face_encodings)
        data = {
            'name': [name],
            'classes': [classes],
            'face_encodings': [encoding_json]
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def read(self, student_id=None):
        """Read a student record using pandas."""
        if student_id:
            df = pd.read_sql_query(f"SELECT * FROM student WHERE id = {student_id}", self.conn)
            if not df.empty:
                df['face_encodings'] = df['face_encodings'].apply(json.loads)
            return df
        else:
            df = pd.read_sql_query("SELECT * FROM student", self.conn)
            if not df.empty:
                df['face_encodings'] = df['face_encodings'].apply(json.loads)
            return df

    def read_all(self):
        """Read all student records using pandas."""
        df = pd.read_sql_query("SELECT * FROM student", self.conn)
        if not df.empty:
            df['face_encodings'] = df['face_encodings'].apply(json.loads)
        return df

    def update(self, student_id, name, classes, face_encodings):
        """Update a student record using pandas."""
        encoding_json = json.dumps(face_encodings)
        data = {
            'id': student_id,
            'name': name,
            'classes': classes,
            'face_encodings': encoding_json
        }
        df = pd.DataFrame([data])
        df.to_sql(self.table_name, self.conn, if_exists='replace', index=False, method='multi', chunksize=1000)

    def delete(self, student_id):
        """Delete a student record using pandas."""
        query = f"DELETE FROM {self.table_name} WHERE id = {student_id}"
        self.execute_query(query)


class AttendanceTable(DatabaseController):
    """Class for managing the 'attendance' table."""
    def __init__(self, db_name:str = None):
        self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database/school.db')
        super().__init__(db_name)
        self.table_name = 'attendance'
        self.connect()
        data = {
            'id': [],
            'class_id': [],
            'student_id': [],
            'date': [],
            'status': []
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def create(self, class_id, student_id, date, status):
        """Create a new attendance record using pandas."""
        if status not in ["Present", "Absent"]:
            raise ValueError("Invalid status. Must be 'Present' or 'Absent'.")
        data = {
            'class_id': [class_id],
            'student_id': [student_id],
            'date': [date],
            'status': [status]
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def read(self, attendance_id=None):
        """Read an attendance record using pandas."""
        if attendance_id:
            return pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE id = {attendance_id}", self.conn)
        else:
            return pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)

    def filter_by_class(self, class_id):
        """Filter attendance records by class ID using pandas."""
        return pd.read_sql_query(f"SELECT * FROM attendance WHERE class_id = {class_id}", self.conn)

    def filter_by_student(self, student_id):
        """Filter attendance records by student ID using pandas."""
        return pd.read_sql_query(f"SELECT * FROM attendance WHERE student_id = {student_id}", self.conn)

    def filter_by_date_range(self, start_date, end_date):
        """Filter attendance records by date range using pandas."""
        return pd.read_sql_query(f"SELECT * FROM attendance WHERE date BETWEEN '{start_date}' AND '{end_date}'", self.conn)

    def update(self, attendance_id, class_id, student_id, date, status):
        """Update an attendance record using pandas."""
        self.execute_query(
            f"UPDATE attendance SET class_id = {class_id}, student_id = {student_id}, date = '{date}', status = '{status}' WHERE id = {attendance_id}"
        )



class FaceTable(DatabaseController):
    """Class for managing the 'face' table."""
    def __init__(self, db_name):
        self.db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database/school.db')
        super().__init__(db_name)
        self.table_name = 'face'
        self.connect()
        data = {
            'id': [],
            'student_id': [],
            'encoding': []
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def create(self, student_id, encoding):
        """Create a new face encoding record using pandas."""
        encoding_json = json.dumps(encoding)
        data = {
            'student_id': [student_id],
            'encoding': [encoding_json]
        }
        df = pd.DataFrame(data)
        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)

    def read(self, face_id=None):
        """Read a face encoding record using pandas."""
        if face_id:
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE id = {face_id}", self.conn)
            if not df.empty:
                df['encoding'] = df['encoding'].apply(json.loads)
            return df
        else:
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)
            if not df.empty:
                df['encoding'] = df['encoding'].apply(json.loads)
            return df

    def find_by_student(self, student_id):
        """Find all face encodings for a student using pandas."""
        df = pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE student_id = {student_id}", self.conn)
        if not df.empty:
            df['encoding'] = df['encoding'].apply(json.loads)
        return df

    def update(self, face_id, student_id, encoding):
        """Update a face encoding record using pandas."""
        encoding_json = json.dumps(encoding)
        self.execute_query(
            f"UPDATE {self.table_name} SET student_id = {student_id}, encoding = '{encoding_json}' WHERE id = {face_id}"
        )

    def delete(self, face_id):
        """Delete a face encoding record using pandas."""
        self.execute_query(f"DELETE FROM {self.table_name} WHERE id = {face_id}")


def main():
    db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../database/school.db')
    # Example usage
    class_table = ClassTable(db_name)
    class_table.create('Math 101', 101, 'Introduction to Mathematics', '2022-01-01', '2022-05-01', '09:00:00')
    print(class_table.read().to_json(orient='records', lines=True))

    # student_table = StudentTable(db_name)
    # student_table.create("Alice Johnson", 1, ["encoding_data"])

    # attendance_table = AttendanceTable(db_name)
    # attendance_table.create(1, 1, "2024-01-16", "Present")

    # face_table = FaceTable(db_name)
    # face_table.create(1, ["face_encoding_data"])


if __name__ == "__main__":
    main()
