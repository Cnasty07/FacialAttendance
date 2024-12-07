CREATE TABLE class (
    class_id INT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    class_room_number INT NOT NULL,
    class_description TEXT,
    class_start_date DATE,
    class_end_date DATE,
    class_time TIME
);

CREATE TABLE student (
    student_id INT PRIMARY KEY, -- Student ID
    student_name VARCHAR(100) NOT NULL, -- Full name
    student_classes JSON, -- Array of class_id
    student_face_data JSON, -- Array of face_id
    FOREIGN KEY (student_classes) REFERENCES class(class_id) -- Foreign key to class table
);

CREATE TABLE attendance (
    attendance_id INT PRIMARY KEY,
    class_id INT,
    student_id INT,
    attendance_date DATE,
    attendance_status VARCHAR(10),
    FOREIGN KEY (class_id) REFERENCES class(class_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE face (
    face_id INT PRIMARY KEY,
    student_id INT,
    face_encoding JSON,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);