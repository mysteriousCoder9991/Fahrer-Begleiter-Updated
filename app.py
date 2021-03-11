"""
# AIM:-  TO ALERT THE DRIVER WHEN HE IS FEELING FATIGUE OR TIRED

#PROGRAM DEVELOPED BY : RAHUL DHAR

#VERSION:-1.0.2.10.07.2019
"""
import os
import sys
from tkinter import *
from tkinter import *

# To import the required packages
import cv2
import playsound
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


# To declare the class
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Fahrer-Beigleiter : An alertness system for drivers'  # To set the title
        self.left = 10  # To set the left border
        self.top = 10  # To set the top border
        self.width = 320  # To set the width
        self.height = 200  # To set the height
        self.initUI()  # To call the initUI() method

    def sleepAlarm(self):  # To define the sleepAlarm method
        top = Tk()
        C1 = Label(top, text="Fahrer-Beigleiter", bg='#A4C639')  # To set the title bar
        C1.pack()
        L1 = Label(top, text="You are going off to sleep!!!", bg='#FFE135')  # To display the message
        L1.pack(side=LEFT)
        top.mainloop()

    def fatigueAlarm(self):  # To define the fatigueAlarm method
        top = Tk()
        C1 = Label(top, text="Fahrer-Beigleiter", bg='#A4C639')  # To set the title bar
        C1.pack()
        L1 = Label(top, text="Your eyes are closed for a long time!!!", bg='#FFE135')  # To display the message
        L1.pack(side=LEFT)
        top.mainloop()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        buttonReply = QMessageBox.question(self, 'Fahrer Beigleiter', "Do you want to use Fahrer-Beigleiter ?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)  # To ask whether he wants to use the system
        if buttonReply == QMessageBox.Yes:  # If the user clicks 'Yes'
            print('Yes clicked')
            playsound.playsound('service-bell.wav')
            face_cascade = cv2.CascadeClassifier('face.xml')  # To load the face haarcascade file
            right_eye_cascade = cv2.CascadeClassifier('rightEye.xml')  # To load the right-eye haarcascade file
            left_eye_cascade = cv2.CascadeClassifier('leftEye.xml')  # To load the left-eye haarcascde file
            if face_cascade.empty() or right_eye_cascade.empty() or left_eye_cascade.empty():
                raise IOError(
                    'Unable to load the required haarcascade file/s')  # To raise an error if the required haarcascade file isn't available
            cap = cv2.VideoCapture(0)  # To set the camera for capture
            ds_factor = 0.5  # To set the scaling factor
            while True:  # To start an infinite loop
                r, frame = cap.read()  # To start the capture from the camera
                frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
                                   interpolation=cv2.INTER_AREA)  # To resize the frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To convert the image into grey scale
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # To run the face detector on the grayscale image
                if len(faces) == 0:  # To check if no faces are found
                    playsound.playsound('airhorn.wav')  # To alert the driver when no faces are found
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (210, 255, 210),
                                  3)  # To draw the rectangle around the face
                roi_gray = gray[y:y + h, x:x + w]  # Extract the gray face ROI
                roi_color = frame[y:y + h, x:x + w]  # Extract the color face ROI
                leftEye = left_eye_cascade.detectMultiScale(roi_gray)  # To detect the left eye from the grayscale face
                rightEye = right_eye_cascade.detectMultiScale(
                    roi_gray)  # To detect the right eye from the grayscale face
                if len(leftEye) == 0 and len(rightEye) == 0:  # To check if both the eyes are closed or not
                    playsound.playsound(
                        'Smoke Alarm.wav')  # To alert the driver if both of the eyes are closed for a long time
                for (x_eye, y_eye, w_eye, h_eye) in leftEye:
                    center = (int(x_eye + 0.5 * w_eye), int(y_eye + 0.5 * h_eye))
                    radius = int(0.3 * (w_eye + h_eye))
                    color = (0, 255, 0)
                    thickness = 3
                    cv2.circle(roi_color, center, radius, color, thickness)  # To draw the circles around the left eye
                for (x_eye, y_eye, w_eye, h_eye) in rightEye:
                    center = (int(x_eye + 0.5 * w_eye), int(y_eye + 0.5 * h_eye))
                    radius = int(0.3 * (w_eye + h_eye))
                    color = (0, 0, 255)
                    thickness = 3
                    cv2.circle(roi_color, center, radius, color, thickness)  # To draw the circle around the right eye

                cv2.imshow(' Fahrer Begleiter--An alertness system for Drivers ',
                           frame)  # To show the captured frame to the user
                c = cv2.waitKey(1)  # To accept user's input to continue or not
                if c == 27:  # To check if the 'esc' key is pressed
                    break
            cap.release()  # To release the allocated memory space
            cv2.destroyAllWindows()  # To destroy all the windows
            print("\nThank You for using Fahrer Begleiter\nThis system is developed by Rahul Dhar")
        else:
            exit()  # To exit from the system


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
