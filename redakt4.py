#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
#from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)


import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests
import asyncio
import aiohttp

import uuid

import section_screen
import section_edit
import faculties_screen
import global_constants
from sections_api import FullArticleInfo, ArticleApi
from preloader import Preloader


class EditorWindow(QMainWindow, QWidget):# класс MainWindow

    def __init__(self, article_id=None, parent_id=9, article_name=None, *args, **kwargs):
        super(EditorWindow, self).__init__(*args, **kwargs)
       #виджет отображает область редактирования
        self.api = ArticleApi(global_constants.ARTICLE_API)
        self.article_id = article_id
        self.parent_id = parent_id
        self.article_name = article_name
        self.photo_urls_list = None
        self.article_text = None

        self.new_photoes = []
        #self.photo_filenames_list = []
        if self.article_id is None:
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


    def add_delete_button(self):
        self.button_delete = QPushButton("Удалить статью")
        #self.button_delete.setText("Удалить")
        self.button_delete.setFont(self.button_font)
        self.button_delete.setIcon(QIcon("images/bin.png"))
        self.button_delete.setIconSize(QSize(20,20))
        #self.button_delete.setMaximumWidth(50)
        self.button_delete.clicked.connect(self.delete_article)
        self.head_layout.addWidget(self.button_delete)


    def init_ui(self):
        self.resize(800,600)

        self.button_font = QFont()
        self.button_font.setPointSize(10)

        layout = QVBoxLayout()

        self.head_layout = QHBoxLayout()
        
        self.label_nazvprot = QLabel("Введите название для статьи:")
        self.head_layout.addWidget(self.label_nazvprot)
        self.head_layout.addStretch()

        layout.addLayout(self.head_layout)
        
        if (self.article_id):
            self.add_delete_button()

        self.label_nazv = QLineEdit(self)
        fixedfontnazv = QFont() #QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(14)
        self.label_nazv.setFont(fixedfontnazv)
        if self.article_name:
            self.label_nazv.setText(self.article_name)
        layout.addWidget(self.label_nazv)
        
        self.editor = QTextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        #self.editor.selectionChanged.connect(self.update_format)

        font = QFont('Times', 12)
        self.editor.setFont(font)

        self.editor.setFontPointSize(12) 

        if self.article_text:
            self.editor.setPlainText(self.article_text)

        # self.path(содержит путь к текущему открытому файлу)
        # Если "None", получается, что файл еще не открыт (или создается новый).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        
        #file_menu = self.menuBar().addMenu("&File")

        self.razdel = QPushButton('Переход в создание раздела')
        #self.razdel.clicked.connect(self.buttonClicked)

        image_buttons_layout = QHBoxLayout()

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)
        image_buttons_layout.addWidget(self.button_open)

        self.clear_all = QPushButton('Отчистить картинки')
        self.clear_all.clicked.connect(self.clear_images)
        image_buttons_layout.addWidget(self.clear_all)

        self.button_edit_article = QPushButton('Создать статью')
        if self.article_id:
            self.button_edit_article.setText('Отправить изменения')
        self.button_edit_article.clicked.connect(self.edit_article_event)

        #scroll section
        self.scrollLayout = QHBoxLayout()
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scroller = QScrollArea()
        #self.setCentralWidget(self.scroller)
        #self.scroller.setFixedWidth(650)
        self.scroller.setFixedHeight(120)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        
        self.scroller.setWidget(self.scrollWidget)
        self.label_images = []
        self.scrollLayout.addStretch()
        #self.label_image = QLabel("<Здесь будут отображаться фотографии, которые Вы выбрали>")
       
        layout.addWidget(self.razdel)
        #layout.addWidget(self.button_open)
        layout.addLayout(image_buttons_layout)
        layout.addWidget(self.scroller)
        layout.addWidget(self.button_edit_article)

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
        
        
        #file_menu.addAction(open_file_action)
        
        #file_menu.addAction(save_file_action)


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


    def sections_list_action_triggered(self):
        self.sections_window = section_screen.SectionsWindow()
        self.sections_window.move(self.pos())
        self.sections_window.resize(self.size())
        self.sections_window.show()
        self.close()
        #self.destroy()

    
    def section_edit_action_triggered(self):
        #print("clicked!")
        self.section_edit_window = section_edit.SectionEditWindow()
        self.section_edit_window.move(self.pos())
        self.section_edit_window.resize(self.size())
        self.section_edit_window.show()
        self.close()
        #self.destroy()

    
    def switch_to_faculty(self):
        self.faculties_window = faculties_screen.FacultiesWindow()
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()


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

        self.sections_list_action = QtWidgets.QAction(self)
        self.sections_list_action.setObjectName("sectionslistaction")
        self.sections_list_action.triggered.connect(self.sections_list_action_triggered)
        
        self.section_creation = QtWidgets.QAction(self)
        self.section_creation.setObjectName("action_2")
        self.section_creation.triggered.connect(self.section_edit_action_triggered)

        #self.article_creation = QtWidgets.QAction(self)
        #self.article_creation.setObjectName("action_3")
        #self.article_creation.triggered.connect(self.redakt_action_triggered)
        
        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        self.faculty_action.triggered.connect(self.switch_to_faculty)

        self.menu_screens.addAction(self.sections_list_action)
        self.menu_screens.addAction(self.section_creation)
        #self.menu_screens.addAction(self.article_creation)
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Редактирование статьи"))
        self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sections_list_action.setText(_translate("MainWindow", "Список разделов"))
        self.section_creation.setText(_translate("MainWindow", "Создание раздела"))
        #self.article_creation.setText(_translate("MainWindow", "Создание статьи"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))


    def dialog_critical(self, s):#обработка MessageBox
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


    def showEvent(self, event):
        if (self.article_id):
            asyncio.ensure_future(self.init_content())


    def closeEvent(self, event):
        import os, shutil
        folder = 'tempfiles/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

     
#определяем file_open метод, который при запуске использует QFileDialog.getOpenFileName
#для отображения диалогового окна открытия файла платформы
#выбранный путь затем используется для открытия файла 
#
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

    #def buttonClicked(self):
        #self.exPopup = NewWindow()
        #self.exPopup.setWindowTitle("Создание раздела")
        #self.exPopup.setGeometry(100, 200, 100, 100)
        #self.exPopup.show()


    async def init_content(self):
        full_info = await self.api.get_article(self.article_id)
        self.article_name = full_info.article_title
        self.article_text = full_info.article_text
        self.parent_id = full_info.parent_id
        self.photo_urls_list = full_info.pictures_urls

        photoes = []
        async with aiohttp.ClientSession() as session:
            photoes = await full_info.get_images(session)

        self.preloader.stop_loader_animation()
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        for photo in photoes:
            self.add_image(photo)
        


    def add_image(self, filename):
        pixmap = QPixmap(filename)
        label_image = QLabel()
        label_image.setPixmap(pixmap)
        label_image.setScaledContents(True)
        label_image.setMaximumWidth(75)
        label_image.setMinimumHeight(75)
        self.label_images.append(label_image)
        self.scrollLayout.insertWidget(self.scrollLayout.count()-1, label_image)


    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        #print(file_name)
        if not file_name:
            return

        #filepath = file_name.split("/")[-1]
        #file_name1 = file_name.resize((10, 10))

        self.new_photoes.append(file_name)

        self.add_image(file_name)
        


    def clear_images(self):
        #print("clear")
        #self.photo_filenames_list.clear()
        if self.photo_urls_list:
            self.photo_urls_list = None
        if self.new_photoes:
            self.new_photoes.clear()
        for label_image in self.label_images:
            self.scrollLayout.removeWidget(label_image)
        self.label_images.clear()


#функция для отправления все на сервер
    def edit_article_event(self):
        print("edit article")
        if self.photo_urls_list is None:
            self.photo_urls_list = []
        for filename in self.new_photoes:
            try:
                url = get_photo_uri(filename)
                self.photo_urls_list.append(url)
            except Exception as e:
                print("error")
                self.status.showMessage("Ошибка при отправке фотографий!")
        if self.article_id:
            j = {
                    "id": self.article_id,
                    "isMain" : False,
                    "title" : str(self.label_nazv.text()),
                    "text": self.editor.toPlainText(),
                    "parentId": self.parent_id,
                    "pictures": self.photo_urls_list
                }
            url = global_constants.ARTICLE_API
            try:
                res = requests.put(url, json=j)
                self.status.showMessage("Статья отправлена")
                
            except Exception as e:
                self.status.showMessage("Ошибка при отправке статьи")
        else:
            j = {
                    "isMain" : False,
                    "title" : str(self.label_nazv.text()),
                    "text": self.editor.toPlainText(),
                    "parentId": self.parent_id,
                    "pictures": self.photo_urls_list
                }
            url = global_constants.ARTICLE_API
            try:
                res = requests.post(url, json=j)
                self.status.showMessage("Статья отправлена")
                self.button_edit_article.setText("Отправить изменения")
                self.article_id = res.json()['id']
                self.add_delete_button()
            except Exception as e:
                self.status.showMessage("Ошибка при отправке статьи")


    def delete_article(self):
        if self.article_id is None:
            return
        #payload = {'id': self.sect_id}
        try:
            r = requests.delete(global_constants.ARTICLE_API+f"/{self.article_id}")
            if (r.status_code == 200):
                self.status.showMessage("Статья удалена!")
                self.sections_list_action_triggered()
            else:
                self.status.showMessage("Ошибка при удалении!")
                print(r.status_code)
        except Exception as e:
            self.status.showMessage("Ошибка при отправке запроса!") 


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
            #print(f'Нужный url: {url_data["url"]}')
            return url_data["url"]


#результат
if __name__ == '__main__':
#конец программы
    app = QApplication(sys.argv)
    app.setApplicationName("Редактор статьи")
    window = EditorWindow()
    window.show()
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