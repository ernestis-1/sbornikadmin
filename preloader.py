import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie

class Preloader(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)
        #self.setFixedSize(260,260)

        self.loader = QLabel(self)
        self.loader_animation = QMovie("images/giphy.gif")
        self.loader.setMovie(self.loader_animation)
        self.start_loader_animation()

    def start_loader_animation(self):
        self.loader_animation.start()

    def stop_loader_animation(self):
        self.loader_animation.stop()

#app = QApplication(sys.argv)
#preloader = Preloader()
#preloader.show()
#sys.exit(app.exec_())