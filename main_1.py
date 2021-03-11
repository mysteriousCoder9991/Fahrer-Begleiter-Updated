import sys
from tkinter import *

import cv2
import playsound
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Fahrer-Beigleiter : An alertness system for drivers'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def sleepAlarm():
        top = Tk()
        C1 = Label(top, text="Fahrer-Beigleiter", bg='#A4C639')
        C1.pack()
        L1 = Label(top, text="You are going off to sleep!!!", bg='#FFE135')
        L1.pack(side=LEFT)
        top.mainloop()

    def fatigueAlarm():
        top = Tk()
        C1 = Label(top, text="Fahrer-Beigleiter", bg='#A4C639')
        C1.pack()
        L1 = Label(top, text="Your eyes are closed for a long time!!!", bg='#FFE135')
        L1.pack(side=LEFT)
        top.mainloop()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        buttonReply = QMessageBox.question(self, 'Fahrer Beigleiter', "Do you want to use Fahrer-Beigleiter ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked')
            playsound.playsound('service-bell.wav')
            face_cascade = cv2.CascadeClassifier('face.xml')
            right_eye_cascade = cv2.CascadeClassifier('rightEye.xml')
            left_eye_cascade = cv2.CascadeClassifier('leftEye.xml')
            if face_cascade.empty() or right_eye_cascade.empty() or left_eye_cascade.empty():
                raise IOError('Unable to load')
            cap = cv2.VideoCapture(0)
            ds_factor = 0.5
            while True:
                r, frame = cap.read()
                frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To convert the image into grey scale
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # To run the face
                if len(faces) == 0:
                    playsound.playsound('airhorn.wav')
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (210, 255, 210), 3)  # To d
                roi_gray = gray[y:y + h, x:x + w]  # Extract the gray face ROI
                roi_color = frame[y:y + h, x:x + w]  # Extract the color face ROI
                leftEye = left_eye_cascade.detectMultiScale(roi_gray)
                rightEye = right_eye_cascade.detectMultiScale(roi_gray)
                if len(leftEye) == 0 and len(rightEye) == 0:
                    playsound.playsound('Smoke Alarm.wav')
                for (x_eye, y_eye, w_eye, h_eye) in leftEye:
                    center = (int(x_eye + 0.5 * w_eye), int(y_eye + 0.5 * h_eye))
                    radius = int(0.3 * (w_eye + h_eye))
                    color = (0, 255, 0)
                    thickness = 3
                    cv2.circle(roi_color, center, radius, color, thickness)  # To draw the circles around the eyes
                for (x_eye, y_eye, w_eye, h_eye) in rightEye:
                    center = (int(x_eye + 0.5 * w_eye), int(y_eye + 0.5 * h_eye))
                    radius = int(0.3 * (w_eye + h_eye))
                    color = (0, 0, 255)
                    thickness = 3
                    cv2.circle(roi_color, center, radius, color, thickness)

                cv2.imshow(' Fahrer Begleiter--An alertness system for Drivers ', frame)
                c = cv2.waitKey(1)
                if c == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            print("\nThank You for using Fahrer Begleiter\nThis system is developed by Rahul Dhar")
        else:
            exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
