#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)


import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests

import uuid

class NewWindow(QMainWindow, QWidget):
    def __init__(self, *args, **kwargs):
        super(NewWindow, self).__init__()
        main_layout = QVBoxLayout()

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

       
        

        self.label_nazvprot = QLabel("Введите имя контакта:")

        self.label_telefonprot = QLabel("Введите телефон контакта:")

        self.label_postprot = QLabel("Введите должность контакта:")

        self.label_nazv = QLineEdit()#QPlainTextEdit
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)

        self.label_telefon = QLineEdit()#QPlainTextEdit
        fixedfonttelefon = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfonttelefon.setPointSize(18)
        self.label_telefon.setFont(fixedfonttelefon)

        self.label_post = QLineEdit()#QPlainTextEdit
        fixedfontpost = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontpost.setPointSize(18)
        self.label_post.setFont(fixedfonttelefon)

        main_layout.addWidget(self.label_nazvprot)
        main_layout.addWidget(self.label_nazv)
        main_layout.addWidget(self.label_telefonprot)
        main_layout.addWidget(self.label_telefon)
        main_layout.addWidget(self.label_postprot)
        main_layout.addWidget(self.label_post)

        self.setLayout(main_layout)

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        filepath = file_name.split("/")[-1]
        
        background = QPixmap(file_name).scaled(100,100) 
        #pixmap = QPixmap(file_name)
        self.label_image.setPixmap(background)



if __name__ == '__main__':
    app = QApplication([])

    mw = NewWindow()
    mw.show()

    app.exec()









        
