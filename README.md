# Facial Recognition Attendance System

- by Chris Nastasi & Ruben Reyes

## Description

This project aims to create a facial attendance system that detects unique faces and updates attendance values in the database for specific classes and specific students.

## Overview

A Python-based facial recognition system for managing and recording student attendance. It utilizes machine learning for face detection and recognition, integrated with a SQLite database for data management, and provides a user-friendly GUI built with Tkinter.

## Features

- **Face Detection and Recognition**: Identifies and verifies student faces using `face_recognition` and `dlib`.
- **Database Management**: Handles student and attendance records with SQLite.
- **User Interface**: Interactive GUI for capturing images and confirming attendance.
- **Modular Architecture**: Organized codebase with separate modules for components and controllers.
- **Unit Testing**: Ensures code reliability with comprehensive tests.

## Project Structure

### Database Structure

- DATABASE SYSTEMS

```

    Class {
        class_id: int, PK
        room_num: int
        class_name: string
        class_description: string
        start_date: date
        end_date: date
        schedule: string
    }
    Student {
        student_id: int, PK
        class_id: int, FK
        student_name: string
    }
    Attendance {
        attendance_id: int, PK
        student_id: int, FK
        class_id: int, FK
        date: date
        status: boolean
    }

```

Programming Languages:
