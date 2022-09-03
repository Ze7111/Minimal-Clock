import threading
from src.acrylic import WindowEffect

try:
	import PySide2
except Exception as e:
    import os
    string = str(e)
    module = string.split("'")[1].split("'")[0]
    os.system(f'pip install {module}')

from PySide2.QtWidgets import QWidget, QApplication
from src.acrylic import WindowEffect  # import the module
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
import sys; from time import strftime, sleep

innit: bool = False
stop_threads: bool = False
scw, sch = 0, 0


class Window(QWidget):
    def __init__(self):
        global scw, sch
        super(Window, self).__init__()
        screen = app.primaryScreen()
        size = screen.size()
        scw, sch = size.width(), size.height()
        self.setFixedWidth(scw)
        self.setFixedHeight(sch)
        self.setWindowTitle("Clock")  # set the title of the window
        self.setWindowIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)  # make the window frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # make the window translucent
        #self.setAttribute(Qt.WA_NoSystemBackground, True)  # make the window translucent

        self.ui_layout = QtWidgets.QGridLayout(self)  # create a ui layout
        self.ui_layout.setAlignment(Qt.AlignCenter)  # center the layout
        self.label = QtWidgets.QLabel(f"{strftime('%I:%M:%S %p')}", self)  # create a label to display a text
        self.label.setFont(QFont("Segoe UI Variable Small Semibol", 80))  # configure the text size and font
        self.label.setAlignment(Qt.AlignCenter)  # center the text
        self.label.setStyleSheet("color: rgb(103, 104, 171);")  # set the text color to white
        self.ui_layout.addWidget(self.label)  # add the label widget into the layout
        
        self.windowFX = WindowEffect()  # instatiate the WindowEffect class
        self.windowFX.setAcrylicEffect(self.winId())  # set the Acrylic effect by specifying the window id


def second_process(win):
    while True:
        global stop_threads
        for i in range(100):
            sleep(1)
            win.label.setText(f"{strftime('%I:%M:%S %p')}")
            win.update()
            if stop_threads:
                break
        if stop_threads:
            break
        
def third_process(win):
    while True:
        global stop_threads
        # loop through every hex color smoothly
        red, green, blue = 0, 0, 0
        max=255
        step = 255//155
        for i in range(0, max):
            i += 1
            red = 255 - (i*step)
            green = 0
            blue = 255 - red
            RGBtriplet = (red, green, blue)
            win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});")  # set the text color to white
            print (RGBtriplet)
            win.update()
            sleep(0.01)                
            if stop_threads:
                break
        if stop_threads:
                break

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = win = Window()
        win.show()
        p2 = threading.Thread(target=second_process, args=(win,)).start()
        #p3 = threading.Thread(target=third_process, args=(win,)).start()
        app.exec_()
    finally:
        stop_threads = True
        sys.exit(1)