from setuptools import setup, find_packages

setup(
    name='FacialAttendance',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'dlib',
        'face_recognition',
        'pandas', 
        'scikit-learn',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'facialattendance=facialattendance.__main__:main',
        ],
    },
    author='Chris Nastasi & Ruben Reyes',
    author_email='cnast01@jaguar.tamu.edu',
    description='A facial recognition based attendance system',
    url='https://github.com/Cnasty07/FacialAttendance',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)