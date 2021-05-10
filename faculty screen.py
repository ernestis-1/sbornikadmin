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
from PIL import Image



import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests

import uuid

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        self.label_nazvprot = QLabel("Введите название для статьи:")

        self.label_nazv = QLineEdit()#QPlainTextEdit
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)

        self.editor = QTextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        

        font = QFont('Times', 12)
        self.editor.setFont(font)

        self.editor.setFontPointSize(12)


        
        

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)

        #self.label_image = QLabel()

        

        self.label_image = QLabel('<Здесь будет фотография, которую Вы прикрепите>')

        self.button_save_as = QPushButton('Отправить изменения')
        self.button_save_as.clicked.connect(self._on_save_as_image)

        

       


        # Путь сохранения файла
        self.save_file_name = 'C:\img.jpg'


        main_layout.addWidget(self.label_nazvprot)
        main_layout.addWidget(self.label_nazv)
        main_layout.addWidget(self.editor)
        main_layout.addWidget(self.button_open)
        main_layout.addWidget(self.label_image)
        main_layout.addWidget(self.button_save_as)
        
        
       
        
        self.resize(700, 600)
        self.setLayout(main_layout)
                                     

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        filepath = file_name.split("/")[-1]
        
        background = QPixmap(file_name).scaled(100,100) 
        #pixmap = QPixmap(file_name)
        self.label_image.setPixmap(background)

    def _on_save_as_image(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", 'img.jpg', "Image (*.png *.jpg)")[0]
        if not file_name:
            return
        
        self.label_image.pixmap().save(file_name)



    def file_saveas(self):#функция для сохранения файла как
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt All files (*.*)")

        if not path:
            # Если было отменено, то вернется - ''
            return

        self._save_to_path(path)




if __name__ == '__main__':
    app = QApplication([])

    mw = NewWindow()
    mw.show()

    app.exec()
