import threading
from src.acrylic import WindowEffect
from src.r_config import Read # import the module for reading the config file
read = Read().get_default # read the config file
if read('FirstLaunch') == 'True' or read('FirstLaunch') == 'Backup-Used': # if the FirstLaunch variable is True or Backup-Used
    from src.FirstLaunch import setup # import the setup class
    setup().write_to_file() # write the config file
    exit()


if read('AutoUpdate') == 'True':
    from src.update import main
    main()
try:
    import PySide2, configparser, ctypes # type: ignore
    myappid = 'ze7111holdings.minimalclock.clock.100' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) # set the app id
except Exception as e: # if the user doesn't have PySide2 installed
    import os # type: ignore
    string = str(e) # convert the error to a string
    module = string.split("'")[1].split("'")[0] # get the module name
    os.system(f'pip install {module}') # install the module

from PySide2.QtWidgets import QWidget, QApplication # type: ignore
from src.acrylic import WindowEffect  # import the module for the clock
from PySide2 import QtWidgets # type: ignore
from PySide2.QtCore import Qt # type: ignore
from PySide2.QtGui import QFont, QIcon # type: ignore
import sys; from time import strftime, sleep # import the time module


innit: bool = False # if the window has been initialized
stop_threads: bool = False # set the stop_threads variable to False
scw, sch = 0, 0 # screen width and height


class Window(QWidget): # create a class for the window
    def __init__(self): # the __init__ function
        global scw, sch # make the screen width and height variables global
        super(Window, self).__init__() # call the super class
        screen = app.primaryScreen() # get the screen
        size = screen.size() # get the size of the screen
        scw, sch = size.width(), size.height() # set the screen width and height variables
        self.setFixedWidth(scw); self.setFixedHeight(sch) # set the window size
        self.setWindowTitle(read('AppName')); self.setWindowFlags(Qt.FramelessWindowHint); self.setAttribute(Qt.WA_TranslucentBackground) # set the window title, flags, and background
        self.setWindowIcon(QIcon('assets/icon.ico')) # set the window icon
        self.ui_layout = QtWidgets.QGridLayout(self)  # create a ui layout
        self.ui_layout.setAlignment(Qt.AlignCenter)  # center the layout
        if read('Text') == '<time>': self.label = QtWidgets.QLabel(f"{strftime(read('TimeFormat'))}", self)  # create a label to display a text
        else: self.label = QtWidgets.QLabel(f"{read('Text')}", self)
        self.label.setFont(QFont(read('Font'), int(read('FontSize'))))  # configure the text size and font
        self.label.setAlignment(Qt.AlignCenter)  # center the text
        self.label.setStyleSheet(f"color: {read('FontColor')};")  # set the text color to white
        self.ui_layout.addWidget(self.label)  # add the label widget into the layout
        self.windowFX = WindowEffect()  # instatiate the WindowEffect class
        self.windowFX.setAcrylicEffect(self.winId())  # set the Acrylic effect by specifying the window id

def second_process(win):
    while True: # create a loop
        global stop_threads # make the stop_threads variable global
        for i in range(100): # loop through every hex color smoothly
            sleep(1) # sleep for 1 second
            win.label.setText(f"{strftime(read('TimeFormat'))}"); win.update() # update the text and the window
            if stop_threads: break # if the stop_threads variable is True, break the loop
        if stop_threads: break # if the stop_threads variable is True, break the loop
        
def third_process(win):
    while True: # create a loop
        global stop_threads # make the stop_threads variable global
        # loop through every hex color smoothly
        red, green, blue = 0, 0, 0 # set the red, green, and blue variables to 0
        max=255 # max value for each color
        step = 255//155 # 255/155 = 1.64
        for i in range(0, max): # red
            i += 1 # increment the i variable
            red = 255 - (i*step); green = 0 # set the red and green values
            blue = 255 - red; RGBtriplet = (red, green, blue) # set the RGB triplet
            win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});"); win.update(); sleep(0.01) # update the text         
            if stop_threads: break # if the stop_threads variable is True, break the loop
        if stop_threads: break # if the stop_threads variable is True, break the loop

if __name__ == "__main__": # if the file is being run
    try: # try to run the code
        app = QApplication(sys.argv) # create an application
        window = win = Window() # create a window
        win.setWindowIcon(QIcon(r'.\src\icon.png')); win.show() # set the window icon and show the window 
        if read('Text') == '<time>': threading.Thread(target=second_process, args=(win,)).start() # start the second process
        if read('FontColor') == '<rainbow>': threading.Thread(target=third_process, args=(win,)).start() # start the thread
        app.exec_() # run the application
    finally: # if the code fails
        stop_threads = True # set the stop_threads variable to True
        os.system('pause') # pause the program