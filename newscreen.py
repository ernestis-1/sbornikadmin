#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont, QIcon

import os #работа с операционной системой
import sys#модуль sys(список аргументов командной строки)

        
        

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        title_layout = QVBoxLayout()

        self.line_input_head = QLineEdit()#QPlainTextEdit
        #font_head = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font_input = QFont()
        font_input.setPointSize(14)
        self.line_input_head.setFont(font_input)

        font_head = QFont()
        font_head.setPointSize(12)

        self.label_head = QLabel("Введите название раздела:")
        self.label_head.setFont(font_head)

        self.button_create = QPushButton('Создать раздел')
        self.button_create.setFont(font_head)
        self.button_create.setMinimumHeight(50)

        title_layout.addWidget(self.label_head)
        title_layout.addWidget(self.line_input_head)
        #title_layout.addStretch()
        title_layout.addWidget(self.button_create)
        title_layout.addStretch()


        attachment_layout = QVBoxLayout()

        self.label_image = QLabel()
        self.label_image.setScaledContents(True)
        self.label_image.setMaximumWidth(175)
        self.label_image.setMaximumHeight(175)
        self.label_image.setMinimumWidth(175)
        self.label_image.setMinimumHeight(175)
        pixmap = QPixmap("images/attach.png")
        self.label_image.setPixmap(pixmap)

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)
        self.button_open.setMaximumWidth(200)

        attachment_layout.addWidget(self.label_image)
        attachment_layout.addWidget(self.button_open)
        attachment_layout.addStretch()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(attachment_layout)
        horizontal_layout.addLayout(title_layout)

        #self.controlWidget = QWidget()
        #self.controlWidget.setLayout(horizontal_layout)
        #self.controlWidget.setMinimumHeight(100)


        main_layout = QVBoxLayout()

        
        #self.button_create.clicked.connect(self._on_save_as_image)
        
        main_layout.addLayout(horizontal_layout)
        #main_layout.addWidget(self.controlWidget)
        #main_layout.addWidget(self.button_create)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        pixmap = QPixmap(file_name)
        self.label_image.setPixmap(pixmap)



if __name__ == '__main__':
    app = QApplication([])

    mw = NewWindow()
    mw.show()

    app.exec()
