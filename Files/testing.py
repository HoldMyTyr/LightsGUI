import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

class VideoStreamWidget(QWidget):
    def __init__(self, url, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Webcam Stream')
        self.setGeometry(100, 100, 640, 480)

        # Layout setup
        self.video_layout = QVBoxLayout()
        self.setLayout(self.video_layout)

        # QLabel to display video frames
        self.video_label = QLabel(self)
        self.video_layout.addWidget(self.video_label)

        # Initialize video capture
        self.capture = cv2.VideoCapture(url)

        # Timer for updating the video frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update frame every 30 ms

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
            # Display the image
            self.video_label.setPixmap(QPixmap.fromImage(q_image))
        else:
            print("Failed to retrieve frame from video stream.")

def main():
    app = QApplication(sys.argv)

    # Define the IP list and index
    ipList = ['192.168.1.125', '192.168.1.115']
    x = 1  # Index to select which IP to use

    # Construct the URL
    url = f'http://{ipList[x]}/webcam/?action=stream'

    viewer = VideoStreamWidget(url)
    viewer.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
