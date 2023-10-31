import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QTextEdit
import handTrackingModule as hmt
from sagemakerConnection import get_prediction

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.cap = cv2.VideoCapture(0)
        self.detector = hmt.HandDetector()

        # Set up a timer to capture frames and update the window
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.text_box = QTextEdit(self)
        self.text_box.setFixedHeight(100)  # Adjust the height as needed
        # Set the font size and text alignment
        self.text_box.setStyleSheet("font-size: 60px; text-align: center;")
        self.layout.addWidget(self.text_box)

        self.central_widget.setLayout(self.layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Camera App")
        self.show()

    def update_frame(self):
        success, img = self.cap.read()
        img = cv2.flip(img, 1)
        img = self.detector.findHands(img)
        className = ""
        lmList = self.detector.findPosition(img, draw=False)
        lmDist = []
        lmDist.append(0)

        if len(lmList) != 0:
            # Calculate the distance between points
            for i in range(1, len(lmList)):
                lmDist.append(((lmList[i][0] - lmList[0][0])**2 + (lmList[i][1] - lmList[0][1])**2)**0.5)
            # Predict gesture
            prediction = get_prediction([lmDist])

            if prediction:
                className = prediction

        # Display the image with text
        # cv2.putText(img, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        #
        # Convert the OpenCV image to a format suitable for Qt
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        self.label.setPixmap(pixmap)

        # Update the text box with the prediction
        self.text_box.setPlainText(className)

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    app = QApplication(sys.argv)
    window = CameraApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
