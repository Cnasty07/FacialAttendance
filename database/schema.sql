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
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    student_classes INT,
    student_face_data JSON,
    FOREIGN KEY (student_classes) REFERENCES class(class_id)
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