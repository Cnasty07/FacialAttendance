import os
import cv2
import dlib
import face_recognition
import tkinter as tk
from ui import new_interface
from controllers import facial_controller , databaseController

# local imports 
try:
    from controllers import facial_controller , databaseController
    from ui import new_interface
except ImportError:
    print("Error: Could not import local modules.")

### TODO: Finish Entry to application

#main code 
def activate(root):
    """_summary_
    starts the facial recognition system.
    """
    # adds the CUDA path to the system path and sets dlib to use CUDA
    try : 
        os.add_dll_directory(os.environ['CUDA_PATH'])
        dlib.DLIB_USE_CUDA = True
    except :
        
        print("Cuda not detected. Defaulting to cpu.")
    

    
    # starts the interface
    check_in = new_interface.FacialAttendanceSystemApp(root)
    root.protocol("WM_DELETE_WINDOW", check_in.close)
    root.mainloop()


def deactivate():
    exit()
    

def main():
    activate(tk.Tk())

if __name__ == '__main__':
    main() 
