import sys
import cv2
import msvcrt
import os

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, \
    QProgressBar, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage

ipList = []
keyList = []
nameList = []
currentWebcams = []


def updateLists():
    global ipList
    global keyList
    global nameList

    with open(r'Files\printers.txt', 'r') as file:
        data = file.read()

    printers = data.split('\n')
    if printers[-1] == '':
        printers.pop()

    for x in range(len(printers)):
        ipList.append(printers[x].split(',')[0])
        keyList.append(printers[x].split(',')[1])
        nameList.append(printers[x].split(',')[2])


def getStatus():
    with open(r'Files\temp.txt', 'r') as file:
        msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, os.path.getsize(r'Files\temp.txt'))
        data = file.read()
        # msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(r'Files\temp.txt'))


    returnedData = data.split(r'\n')
    if returnedData[-1] == '':
        returnedData.pop()
    return data.split("\n")


class PrinterStatusWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.namesLayout = QVBoxLayout()
        self.statusColorLayout = QVBoxLayout()
        self.statusLayout = QVBoxLayout()
        self.completionLayout = QVBoxLayout()

        self.printerStatusLayout = QHBoxLayout(self)
        self.printerStatusLayout.addLayout(self.namesLayout)
        self.printerStatusLayout.addLayout(self.statusColorLayout)
        self.printerStatusLayout.addLayout(self.statusLayout)
        self.printerStatusLayout.addLayout(self.completionLayout)

        self.updateStatus()

    def updateStatus(self):
        # clear the layouts
        for i in reversed(range(self.namesLayout.count())):
            namesWidget = self.namesLayout.itemAt(i).widget()
            colorWidget = self.statusColorLayout.itemAt(i).widget()
            statusWidget = self.statusLayout.itemAt(i).widget()
            completionWidget = self.completionLayout.itemAt(i).widget()
            if namesWidget:
                namesWidget.deleteLater()
            if colorWidget:
                colorWidget.deleteLater()
            if statusWidget:
                statusWidget.deleteLater()
            if completionWidget:
                completionWidget.deleteLater()

        # get the status of the printers
        printersStatus = getStatus()

        # add printers names and status to the layout
        for x in range(len(nameList)):
            # configure the current status
            currentStatus = printersStatus[x].split(";")[1]
            #print(currentStatus)

            # configue the names
            nameLabel = QLabel(nameList[x].split("'")[1])

            statusLabel = QLabel(currentStatus.split(" ")[0])

            completionBar = QProgressBar(self)
            completionBar.setMinimum(0)
            completionBar.setMaximum(100)

            if currentStatus == 'Printing':
                percentCompleted = int(round(float(printersStatus[x].split(";")[3])))
                completionBar.setValue(percentCompleted)

                statusLabel.setText('Printing ' + printersStatus[x].split(";")[2][:8])
            else:
                completionBar.setValue(0)

            # add the status color
            size = int(nameLabel.height() / len(nameList))
            if currentStatus == 'Operational' or currentStatus == 'Offline (Error: Connection error, see Terminal tab)':
                pixmap = QPixmap(r'Images\3.png').scaled(size, size)
            elif currentStatus == 'Printing' or currentStatus == 'Paused':
                pixmap = QPixmap(r'Images\2.png').scaled(size, size)
            else:
                pixmap = QPixmap(r'Images\1.png').scaled(size, size)
            pixmapLabel = QLabel(self)
            pixmapLabel.setPixmap(pixmap)

            # adding the widgets
            self.namesLayout.addWidget(nameLabel)
            self.statusColorLayout.addWidget(pixmapLabel)
            self.statusLayout.addWidget(statusLabel)
            self.completionLayout.addWidget(completionBar)
        print('updated')


class PrinterDisplayWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.videoLayout = QHBoxLayout(self)

        self.videoLabel = QLabel(self)
        self.setGeometry(100, 100, 640, 480)

        self.videoLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.videoLayout.addWidget(self.videoLabel)
        self.setLayout(self.videoLayout)

        self.updateUrl()

        self.updateFrame()



    def updateFrame(self):
        ret, frame = self.capture.read()
        if ret:
            height, width, channel = frame.shape
            bytesPerLine = 3*width
            videoImage = QImage(frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
            scaledVideo = QPixmap.fromImage(videoImage).scaled(self.videoLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.videoLabel.setPixmap(scaledVideo)
        else:
            print('Failed to retrieve video stream')

    def updateUrl(self):
        self.url = 'http://192.168.1.115/webcam/?action=stream'
        self.capture = cv2.VideoCapture(self.url)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # name of the window
        self.setWindowTitle('Printer Status')

        # set up the layouts
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        # make and add the printerStatus widget
        printerStatusWidget = PrinterStatusWidget()
        # printerDisplayWidget = PrinterDisplayWidget()
        mainLayout.addWidget(printerStatusWidget)
        # mainLayout.addWidget(printerDisplayWidget)

        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(printerStatusWidget.updateStatus)
        self.timer1.start(10000)

        # self.timer2 = QTimer(self)
        # self.timer2.timeout.connect(printerDisplayWidget.updateFrame)
        # self.timer2.start(30)

        # show the window
        self.show()

    def button_clicked(self):
        updateLists()


if __name__ == '__main__':
    updateLists()

    app = QApplication(sys.argv)

    window = MainWindow()

    getStatus()
    #window.showFullScreen()

    sys.exit(app.exec())



#         button = QPushButton('Click me')
#         #button.setIcon(QIcon('trash.png'))
#         button.clicked.connect(self.button_clicked)
#
#         pixmap = QPixmap(r'Images\4.jpg')
#
#         #movie = QMovie(r'Images\OWait.gif')
#
#         label = QLabel(self)
#         #label.setMovie(movie)
#         label.setPixmap(pixmap)
#         #label.setText('never mind')
#
#         #movie.show()
#
#         label.move(20,30)