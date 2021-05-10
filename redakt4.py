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




class MainWindow(QMainWindow, QWidget):# класс MainWindow

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
       #виджет отображает область редактирования
        layout = QVBoxLayout()
        
        self.photo_list = []
        self.photo_nazvlist =[]

        self.label_nazvprot = QLabel("Введите название для статьи:")

        layout.addWidget(self.label_nazvprot)
        
        self.label_nazv = QLineEdit()
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)
        

        layout.addWidget(self.label_nazv)
        
        self.editor = QTextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        #self.editor.selectionChanged.connect(self.update_format)

        font = QFont('Times', 12)
        self.editor.setFont(font)

        self.editor.setFontPointSize(12)

       
        

        # self.path(содержит путь к текущему открытому файлу)
        # Если "None", получается, что файл еще не открыт (или создается новый).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)


        file_toolbar = QToolBar("File")#файл
        file_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        self.razdel = QPushButton('Переход в создание раздела')
        #self.razdel.clicked.connect(self.buttonClicked)

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)

        self.button_save_as = QPushButton('Отправить картинки')
        self.button_save_as.clicked.connect(self._on_save_as_image)

        


        self.label_image = QLabel("<Здесь будут отображаться фотографии, которые Вы выбрали>")
        self.urlcart1 = QLabel()
        self.urlcart2 = QLabel()
        self.urlcart3 = QLabel()
        self.urlcart4 = QLabel()
        self.urlcart5 = QLabel()
        self.urlcart6 = QLabel()
        self.urlcart7 = QLabel()
        self.urlcart8 = QLabel()
        self.urlcart9 = QLabel()
        self.urlcart10 = QLabel()
        

       
        layout.addWidget(self.razdel)
        layout.addWidget(self.button_open)
        layout.addWidget(self.button_save_as)
        layout.addWidget(self.label_image)
        layout.addWidget(self.urlcart1)
        layout.addWidget(self.urlcart2)
        layout.addWidget(self.urlcart3)
        layout.addWidget(self.urlcart4)
        layout.addWidget(self.urlcart5)
        layout.addWidget(self.urlcart6)
        layout.addWidget(self.urlcart7)
        layout.addWidget(self.urlcart8)
        layout.addWidget(self.urlcart9)
        layout.addWidget(self.urlcart10)
        
      
        
        #.clear()	Очистить выделенный текст
        #.cut() 	Вырезать выделенный текст в буфер обмена
        #.copy()	Копировать выделенный текст в буфер обмена
        #.paste()	Вставить буфер обмена под курсором
        #.undo()	Отменить последнее действие
        #.redo()	Повторить последнее отмененное действие
        #.insertPlainText(text)     Вставить обычный текст под курсором
        #.selectAll()	 Выделить весь текст в документе
        
        # редактор  умеет выполнять множество стандартных операций - копировать, вырезать, вставлять, очищать
        # виджет обеспечивает поддержку всего этого через слоты Qt
        
        # набор кнопок панели инструментов для редактирования, каждая из которых определяется как QAction
        # Подключение .triggeredсигнала от QActionк соответствующему слоту включает определенное поведение
        
        open_file_action = QAction(QIcon(os.path.join('images', 'blueopen.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")#открыть файл
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")#сохранить текущую страницу
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk2.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")#сохранить текущую страницу в указанный файл
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")#напечатать текущую страницу
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")#редактировать
        edit_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'x.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")#отменить последнее изменение
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'redo.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")#повторить последнее изменение
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")#вырезать выбранный текст
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")#копировать выбранный текст
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'paste.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")#вставить
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'all.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'wind.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")#перенос текста в окно
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        

        self.show()

    def dialog_critical(self, s):#обработка MessageBox
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

        
   


   
        
#определяем file_open метод, который при запуске использует QFileDialog.getOpenFileName
#для отображения диалогового окна открытия файла платформы
#выбранный путь затем используется для открытия файла 
#
    def file_open(self):#функция для открытия файла
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
         #конструкции try except
        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

        

    
#два блока для сохранения файлов - save и save_as
#первый для сохранения открытого файла, у которого уже есть имя файла, второй для сохранения нового файла
    def file_save(self):#функция для сохранения файла
        if self.path is None:
            # Если нет пути, то нужно использовать сохранение как
            return self.file_saveas()

        self._save_to_path(self.path)#сохранение

    def file_saveas(self):#функция для сохранения файла как
        #print(self.editor.toPlainText())
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt All files (*.*)")

        if not path:
            # Если было отменено, то вернется - ''
            return

        self._save_to_path(path)
   
        
# в любом случае выполняется само сохранение, _save_to_path()которое принимает целевой путь   
    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:#конструкция try except
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

       
    #настройка печати
    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Текстовый редактор v 0.3" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

    #def buttonClicked(self):
        #self.exPopup = NewWindow()
        #self.exPopup.setWindowTitle("Создание раздела")
        #self.exPopup.setGeometry(100, 200, 100, 100)
        #self.exPopup.show()
        
        
    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        print(file_name)
        if not file_name:
            return

        filepath = file_name.split("/")[-1]
        #file_name1 = file_name.resize((10, 10))
        
        pixmap = QPixmap(file_name)
        
        self.label_image.setText(filepath)
        
        #self.label_image.setPixmap(pixmap)
        
        
        
        
       
        
#функция для отправления все на сервер
    def _on_save_as_image(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", 'img.jpg', "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        self.label_image.pixmap().save(file_name)


def get_photo_uri(path_img):
    url = 'https://api.imgbb.com/1/upload?key=7739426e6cc4b2afe15d5db0e8272009'
    with open(path_img, 'rb') as img:
        name_img = os.path.basename(path_img)
        files = {'image': (name_img,img, 'multipart/form-data', {'Expires': '0'}) }
        with requests.Session() as s:
            r = s.post(url,files=files)
            #print(r.status_code)
            #print(r.text)
            json_response = r.json()
            url_data = json_response['data']
            print(f'Нужный url: {url_data["url"]}')
            return url_data["url"]


#результат
if __name__ == '__main__':
#конец программы
    app = QApplication(sys.argv)
    app.setApplicationName("Текстовый редактор v 0.3")
    window = MainWindow()
    app.exec_()

    
    
#url = http://sbornikbackend.somee.com/GuideSections
#server = 
#   {
#       "isMain" : False,
#       "title" : str(self.label_nazvprot.text())
#       "text":
#       "parentId": 9
#       "pictures":[


#                   ]

#   }
#res = requests.post(url, json=server)
#print res.text


