import os
import cv2
import face_recognition
from datetime import datetime
import numpy as np

class Capture:
    """
    Summary:
        The Capture class provides functionality to capture video and images using OpenCV. 
        It supports three capture methods: 'video', 'image', and 'stored'. The 'video' method 
        captures video frames continuously until the user stops it, the 'image' method captures 
        a single image, and the 'stored' method is used for testing purposes to return a stored image.
    Methods:
        __init__(capture_method: str):
            Initializes the Capture object and starts the appropriate capture method based on the input parameter.
        start_video_capture():
            Captures video frames from the default camera, displays them in a window, and saves the last frame 
            as an image file with a timestamp. The video capture stops when the user presses the 'q' key.
        start_image_capture():
            Captures a single image from the default camera, displays it in a window, and saves it as an image 
            file with a timestamp.
        start_return_image():
            Returns a stored image for testing purposes.
    """
    
    def __init__(self,capture_method: str):
        if capture_method == 'video':
            self.start_video_capture()
        elif capture_method == 'image':
            self.start_image_capture()
        # used for testing
        elif capture_method == 'stored':
             self.start_return_image()
    
    @staticmethod
    def start_video_capture(self) -> np.ndarray:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            cv2.imshow('Video Capture', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
             # Get the current date and time
        now = datetime.now()
        # Format the date and time to include in the file path
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the captured image to the specified path with the timestamp
        file_path = f'./database/captures/captured_image_{timestamp}.jpg'
        # Save the captured image to the specified path
        cv2.imwrite(file_path, frame)
        
        cap.release()
        cv2.destroyAllWindows()
        
        # not sure if this method works on videos yet
        return face_recognition.load_image_file(frame)
    
    @staticmethod
    def start_image_capture() -> np.ndarray:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return
        
        cv2.imshow('Image Capture', frame)
        
        # Get the current date and time
        now = datetime.now()
        # Format the date and time to include in the file path
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the captured image to the specified path with the timestamp
        file_path = f'./database/captures/captured_image_{timestamp}.jpg'
        # Save the captured image to the specified path
        cv2.imwrite(file_path, frame)
        
        
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()
        
        return face_recognition.load_image_file(file_path)

    @staticmethod
    def start_return_image(self):
        return face_recognition.load_image_file('../../database/tests/Musk3.jpg')

def main():
    capture = Capture('stored')
    print(capture)
    

if __name__ == '__main__':
    main() 
