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
    QPushButton, QApplication, QSizePolicy)
#from PIL import Image
#from PyQt5.QtWidgets.QSizePolicy.


import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests
import asyncio
import aiohttp
import uuid

from preloader import Preloader
from sections_api import get_image_path_from_url
import global_constants
import section_screen, faculties_screen
import redakt4
import faculties_screen


class FacultyEditWindow(QMainWindow):
    def __init__(self, fac_id=None, fac_name=None, fac_info=None, img_url=None):
        super().__init__()
        self.resize(800, 600)
        self.fac_id = fac_id
        self.fac_name = fac_name
        self.fac_info = fac_info
        self.img_url = img_url
        self.img_path = None
        if img_url is None:
            self.init_ui()
            self.init_menu()
            self.init_toolbar()
        else:
            self.init_preloader()
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def init_preloader(self):
        self.resize(800,600)
        self.preloader = Preloader()
        self.setCentralWidget(self.preloader)


    async def init_content(self):
        async with aiohttp.ClientSession() as session:
            self.img_path = await get_image_path_from_url(session, self.img_url)

        self.preloader.stop_loader_animation()
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    
    def showEvent(self, event):
        if (self.img_url):
            asyncio.ensure_future(self.init_content())

        
    def init_ui(self):
        self.main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.title_layout = QVBoxLayout()

        head_font = QFont()
        head_font.setPointSize(14)

        self.label_head = QLabel("Введите название факультета:")
        self.label_head.setFont(head_font)

        self.line_input_head = QLineEdit()#QPlainTextEdit
        fixedfontnazv = QFont()#QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.line_input_head.setFont(fixedfontnazv)
        if (self.fac_name):
            self.line_input_head.setText(self.fac_name)


        #send_font = QFont()
        #send_font.setPointSize(15)
        self.button_send = QPushButton('Создать факультет')
        if self.fac_id:
            self.button_send.setText('Отправить изменения')
        self.button_send.setFont(head_font)
        self.button_send.clicked.connect(self.edit_faculty)
        self.button_send.setMinimumHeight(45)


        #self.title_layout.addStretch()
        self.title_layout.addWidget(self.label_head)
        self.title_layout.addWidget(self.line_input_head)
        self.title_layout.addWidget(self.button_send)
        self.title_layout.setAlignment(Qt.AlignTop)
        #self.title_layout.addStretch()



        self.label_image = QLabel()
        self.label_image.setScaledContents(True)
        label_size = 180
        self.label_image.setMaximumWidth(label_size)
        self.label_image.setMaximumHeight(label_size)
        self.label_image.setMinimumWidth(label_size)
        self.label_image.setMinimumHeight(label_size)
        
        
        pixmap = QPixmap("images/attach.png")
        if (self.img_path):
            pixmap = QPixmap(self.img_path)
        self.label_image.setPixmap(pixmap)

        self.button_font = QFont()
        self.button_font.setPointSize(10)

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.setFont(self.button_font)
        self.button_open.clicked.connect(self._on_open_image)
        #self.button_open.setMaximumWidth(label_size)
        
        self.attachment_layout = QVBoxLayout()

        self.attachment_layout.addWidget(self.label_image)
        self.attachment_layout.addWidget(self.button_open)
        self.attachment_layout.setAlignment(Qt.AlignTop)
        #self.attachment_layout.addWidget(self.button_delete)
        #self.attachment_layout.addStretch()
        #attachment_layout.addWidget(self.button_delete)

        if (self.fac_id):
            self.add_delete_button()
        

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(self.attachment_layout)
        horizontal_layout.addLayout(self.title_layout)

        editor_head_layout = QHBoxLayout()
        
        editor_title = QLabel("Info")
        editor_title_font = QtGui.QFont()
        editor_title_font.setPointSize(12)
        editor_title.setFont(editor_title_font)

        editor_head_layout.addWidget(editor_title)


        self.editor = QTextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        editor_font = QFont('Times', 12)
        self.editor.setFont(editor_font)
        self.editor.setFontPointSize(12)
        #self.editor.setMinimumHeight(400)
        if (self.fac_info):
            self.editor.setPlainText(self.fac_info)


        self.title_layout.addLayout(editor_head_layout)
        self.title_layout.addWidget(self.editor)

        self.buttonContacts = QPushButton("Перейти к контактам")
        self.buttonContacts.setFont(head_font)

        self.title_layout.addWidget(self.buttonContacts)


        main_layout.addLayout(horizontal_layout)
        #main_layout.addWidget(self.editor)
        #main_layout.addStretch()       
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)


    def add_delete_button(self):
        self.button_delete = QPushButton("Удалить факультет")
        #self.button_delete.setText("Удалить")
        #font = QFont()
        #font.setPointSize(9)
        #self.button_delete.setFont(font)
        self.button_delete.setFont(self.button_font)
        self.button_delete.setIcon(QIcon("images/bin.png"))
        self.button_delete.setIconSize(QSize(20,20))
        #self.button_delete.setMaximumWidth(175)
        self.button_delete.clicked.connect(self.delete_faculty)
        
        #self.attachment_layout.insertWidget(self.attachment_layout.count()-1, self.button_delete)
        self.attachment_layout.addWidget(self.button_delete)
        #self.attachment_layout.addStretch()

    
    def init_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        self.menu_screens = QtWidgets.QMenu(self.menubar)
        self.menu_screens.setObjectName("menuscreens")
        
        self.menu_modes = QtWidgets.QMenu(self.menubar)
        self.menu_modes.setObjectName("menumodes")
        
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.faculties_list_action = QtWidgets.QAction(self)
        self.faculties_list_action.setObjectName("sectionslistaction")
        self.faculties_list_action.triggered.connect(self.faculties_list_action_triggered)
        
        self.faculty_creation = QtWidgets.QAction(self)
        self.faculty_creation.setObjectName("action_2")
        #self.faculty_creation.triggered.connect(self.add_faculty_clicked)

        #self.article_creation = QtWidgets.QAction(self)
        #self.article_creation.setObjectName("action_3")
        #self.article_creation.triggered.connect(self.redakt_action_triggered)
        
        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        self.sbornic_action.triggered.connect(self.switch_to_sbornic)
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        
        self.menu_screens.addAction(self.faculties_list_action)
        #self.menu_screens.addAction(self.faculty_creation)
        #self.menu_screens.addAction(self.article_creation)
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ScrollArea", "Факультеты"))
        #self.setWindowTitle(_translate("MainWindow", "Редактирование раздела"))
        self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.faculties_list_action.setText(_translate("MainWindow", "Список разделов"))
        self.faculty_creation.setText(_translate("MainWindow", "Создание факультета"))
        #self.article_creation.setText(_translate("MainWindow", "Создание статьи"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))


    def faculties_list_action_triggered(self):
        self.faculties_window = faculties_screen.FacultiesWindow()
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()


    def switch_to_sbornic(self):
        self.sbornic_screen = section_screen.SectionsWindow()
        self.sbornic_screen.move(self.pos())
        self.sbornic_screen.resize(self.size())
        self.sbornic_screen.show()
        self.close()

    
    def init_toolbar(self):
        file_toolbar = QToolBar("File")#файл
        file_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(file_toolbar)

        open_file_action = QAction(QIcon(os.path.join('images', 'blueopen.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")#открыть файл
        open_file_action.triggered.connect(self.file_open)
        #file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")#сохранить текущую страницу
        save_file_action.triggered.connect(self.file_save)
        #file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk2.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")#сохранить текущую страницу в указанный файл
        saveas_file_action.triggered.connect(self.file_saveas)
        #file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")#напечатать текущую страницу
        print_action.triggered.connect(self.file_print)
        #file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")#редактировать
        edit_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(edit_toolbar)
        #edit_menu = self.menuBar().addMenu("&Edit")

        #undo_action = QAction(QIcon(os.path.join('images', 'x.png')), "Undo", self)
        #undo_action.setStatusTip("Undo last change")#отменить последнее изменение
        #undo_action.triggered.connect(self.editor.undo)
        #edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'redo.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")#повторить последнее изменение
        redo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(redo_action)
        #edit_menu.addAction(redo_action)

        #edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")#вырезать выбранный текст
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        #edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")#копировать выбранный текст
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        #edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'paste.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")#вставить
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        #edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'all.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        #edit_menu.addAction(select_action)

        #edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'wind.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")#перенос текста в окно
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        #edit_menu.addAction(wrap_action)


    def edit_faculty(self):
        #print("edit section")
        #s = self.button_create.text()
        if self.fac_id is None:
            self.button_send.setText("Отправить изменения")
            try:
                #print(self.line_input_head.text())
                j = {
                        "name": str(self.line_input_head.text()),
                        "info": self.editor.toPlainText(),
                        "picture": "",
                    }
                if (self.img_path):
                    j["picture"] = redakt4.get_photo_uri(self.img_path)
                #print(j)
                r = requests.post(global_constants.FACULTIES_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Факультет создан!")
                    #print(r.json())
                    self.fac_id = r.json()['id']
                    self.name = r.json()['name']
                    self.add_delete_button()
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка!")
                print(e)
            #self.status.showMessage("Раздел создан!")
        else:
            j = {
                    "id": self.fac_id,
                    "name": str(self.line_input_head.text()),
                    "info": self.editor.toPlainText(),
                    "picture": ""
                }
            if self.img_url:
                j["picture"] = self.img_url
            else:
                if (self.img_path):
                    try:
                        j["picture"] = redakt4.get_photo_uri(self.img_path)
                    except Exception as e:
                        print(e)
                else:
                    pass
            try:
                r = requests.put(global_constants.FACULTIES_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Изменения отправлены!")
                    #print(r.json())
                    self.sect_id = r.json()['id']
                    self.name = r.json()['name']
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка при отправке!")
            #print("section exists")


    def delete_faculty(self):
        if self.fac_id is None:
            return
        #payload = {'id': self.sect_id}
        try:
            r = requests.delete(global_constants.FACULTIES_API+f"/{self.fac_id}")
            if (r.status_code == 200):
                self.status.showMessage("Факультет удалён!")
                self.faculties_list_action_triggered()
            else:
                self.status.showMessage("Ошибка при удалении. Возможно, этот раздел нельзя удалить")
                print(r.status_code)
        except Exception as e:
            #self.print(e.messa)
            self.status.showMessage("Ошибка при отправке запроса!")


    def file_open(self):#функция для открытия файла
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
         #конструкции try except
        if path:
            try:
                with open(path, 'r') as f:
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
        self.setWindowTitle("%s - Редактор статьи" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )


    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return
        
        self.img_path = file_name
        self.img_url = None
        background = QPixmap(file_name) #.scaled(100,100) 
        #pixmap = QPixmap(file_name)
        self.label_image.setPixmap(background)



if __name__ == '__main__':
    app = QApplication([])

    mw = FacultyEditWindow()
    mw.show()

    app.exec()