from src.acrylic import WindowEffect
from src.r_config import Read # import the module for reading the config file
read = Read().get_default # read the config file
if read('FirstLaunch') == 'True' or read('FirstLaunch') == 'Backup-Used': # if the FirstLaunch variable is True or Backup-Used
    from src.FirstLaunch import setup # import the setup class
    setup().write_to_file() # write the config file
    pass

if read('AutoUpdate') == 'True': # if the AutoUpdate variable is True
    try:
        from src.update import main as update # import the update function
        update() # update the program
    except Exception: print('Failed to check for updates') # print failed to update program
     
try: # try to run the program
    import PySide2, configparser, ctypes, subprocess # type: ignore
    myappid = 'ze7111holdings.minimalclock.clock.100' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) # set the app id
except Exception as e: # if the user doesn't have PySide2 installed
    import subprocess, sys # type: ignore
    string = str(e) # convert the error to a string
    module = string.split("'")[1].split("'")[0] # get the module name
    try: # try to install the module
        subprocess.run([sys.executable, "-m", "pip", "install", module]) # install the module
    except Exception as e: # if the user doesn't have pip installed
        print(f'Error: {e}') # print the error
    print("Please restart the program.") # tell the user to restart the program
    sys.exit(0) # exit the program

from PySide2.QtWidgets import QWidget, QApplication # type: ignore
from src.acrylic import WindowEffect  # import the module for the clock
from PySide2 import QtWidgets # type: ignore
from PySide2.QtCore import Qt # type: ignore
from PySide2.QtGui import QFont, QIcon # type: ignore
import sys, os, subprocess, threading # type: ignore
from time import strftime, sleep # import the time module
from src.multithreading import main as startThread # import the startThread function
from src.multithreading import stop_threads, stop_all_threads # import the stop_threads function


innit: bool = False # if the window has been initialized
scw, sch = 0, 0 # screen width and height
show_colors = False # if the colors should be shown


class Window(QWidget): # create a class for the window
    def __init__(self): # the __init__ function
        global scw, sch # make the screen width and height variables global
        super(Window, self).__init__() # call the super class
        screen = app.primaryScreen() # get the screen
        size = screen.size() # get the size of the screen
        scw, sch = size.width(), size.height() # set the screen width and height variables
        self.setFixedWidth(scw) # set the width of the window
        self.setFixedHeight(sch) # set the window size
        self.setWindowTitle(read('AppName')) # set the window title
        self.setWindowFlags(Qt.FramelessWindowHint) # set the window flags
        self.setAttribute(Qt.WA_TranslucentBackground) # set the window title, flags, and background
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


@startThread # start the thread
def second_process(win): # create a function for the second process
    while True: # create a loop
        for i in range(100): # loop through every hex color smoothly
            sleep(1) # sleep for 1 second
            win.label.setText(f"{strftime(read('TimeFormat'))}") # set the text to the current time
            win.update() # update the text and the window
            
            if stop_threads() == True:   # if the stop_threads function returns True
                break # break the loop
        if stop_threads() == True:   # if the stop_threads function returns True
            break # break the loop
 
@startThread # start the thread
def third_process(win): # create a function for the third process
    while True: # create a loop
        red = 0 # set the red variable to 0
        green = 0 # set the red, green, and blue variables to 0
        blue = 0 # set the red, green, and blue variables to 0
        global show_colors # make the show_colors variable global
        for i in range(16777216): # loop through every hex color smoothly
            for i in range(255): # loop through every hex color smoothly
                if red == 255: # if the red color is 255
                    break # break the loop
                red += 1 # add 1 to the red variable
                win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                sleep(0.01) # sleep for 0.01 seconds
                win.update() # update the window
                if show_colors: print(f"rgb({red}, {green}, {blue})") # print the color
                
            for i in range(255): # loop through every hex color smoothly
                if green == 255: # if the green value is 255
                    break # break the loop
                green += 1 # increase the green value
                win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                sleep(0.01) # sleep for 0.01 seconds
                win.update() # update the window 
                if show_colors: print(f"rgb({red}, {green}, {blue})") # print the color
                
            for i in range(255): # loop through every hex color smoothly
                if blue == 255: # if the blue value is 255
                    break # break the loop
                blue += 1 # add 1 to the blue variable
                win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                sleep(0.01) # sleep for 0.01 seconds
                win.update() # update the window 
                if show_colors: print(f"rgb({red}, {green}, {blue})") # print the color
                
            if red == 255 and green == 255 and blue == 255: # if the color is white
                for i in range(255): # loop through every hex color smoothly
                    if red == 0: # if the red value is 0
                        break # break the loop
                    red -= 1 # decrease the red value
                    win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                    sleep(0.01) # set the text color
                    win.update() # update the window
                    if show_colors: print(f"rgb({red}, {green}, {blue})") # print the color
                    
                for i in range(255): # loop through every hex color smoothly
                    if green == 0: # if the green value is 0
                        break # break the loop
                    green -= 1 # set the text color
                    win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                    sleep(0.01) # sleep for 0.01 seconds
                    win.update() # update the window
                    if show_colors: print(f"rgb({red}, {green}, {blue})") # print the color
                    
                for i in range(255):
                    if blue == 0: # if the blue value is 0
                        break # break the loop
                    blue -= 1 # set the text color
                    win.label.setStyleSheet(f"color: rgb({red}, {green}, {blue});") # set the text color
                    sleep(0.01) # sleep for 0.01 seconds
                    win.update() # update the window
                    if show_colors: print(f"rgb({red}, {green}, {blue})")
                
                if stop_threads() == True:  # if the stop_threads function returns True
                    break # break the loop 
            
            if stop_threads() == True:  # if the stop_threads function returns True
                break # break the loop 
        if stop_threads() == True:   # if the stop_threads function returns True
            break # break the loop

if __name__ == "__main__": # if the file is being run
    try: # try to run the code
        app = QApplication(sys.argv) # create an application
        window = win = Window() # create a window
        win.setWindowIcon(QIcon(r'.\src\icon.png'))
        win.show() # set the window icon and show the window 
        if read('Text') == '<time>': second_process(win)
        if read('FontColor') == '<rainbow>': third_process(win) # start the third process
        app.exec_() # run the application
    finally: # if the code fails
        print('Stopping threads...') # print a message
        stop_all_threads()
        sys.exit(0) # exit the program