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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        self.label_nazv = QPlainTextEdit()
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)

       

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)

        self.button_save_as = QPushButton('Сохранить картинку')
        self.button_save_as.clicked.connect(self._on_save_as_image)

        

       

        self.label_image = QLabel()

        self.label_nazvprot = QLabel("Введите название для статьи:")

        # Путь сохранения файла
        self.save_file_name = 'C:\img.jpg'

        
        main_layout.addWidget(self.button_open)
        main_layout.addWidget(self.button_save_as)
        main_layout.addWidget(self.label_image)
        main_layout.addWidget(self.label_nazvprot)
        main_layout.addWidget(self.label_nazv)
       
        

        self.setLayout(main_layout)

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        pixmap = QPixmap(file_name)
        self.label_image.setPixmap(pixmap)

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

    mw = MainWindow()
    mw.show()

    app.exec()
