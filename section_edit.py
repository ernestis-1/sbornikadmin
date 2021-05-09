import os #работа с операционной системой
import sys#модуль sys(список аргументов командной строки)
#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore
#from section_screen import SectionsWindow
import section_screen
import redakt4
import global_constants
import requests

class SectionEditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.init_ui()
        self.init_menu()
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.image_file_name = None


    def init_ui(self):
        title_layout = QVBoxLayout()

        self.line_input_head = QLineEdit(self)#QPlainTextEdit
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
        self.button_create.clicked.connect(self.edit_section_clicked)

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
        #self.setLayout(main_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)


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
        
        #self.section_creation = QtWidgets.QAction(self)
        #self.section_creation.setObjectName("action_2")
        
        self.article_creation = QtWidgets.QAction(self)
        self.article_creation.setObjectName("action_3")
        self.article_creation.triggered.connect(self.redakt_action_triggered)
        
        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        
        self.menu_screens.addAction(self.sections_list_action)
        #self.menu_screens.addAction(self.section_creation)
        self.menu_screens.addAction(self.article_creation)
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Редактирование раздела"))
        self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sections_list_action.setText(_translate("MainWindow", "Список разделов"))
        #self.section_creation.setText(_translate("MainWindow", "Создание раздела"))
        self.article_creation.setText(_translate("MainWindow", "Создание статьи"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return
        self.image_file_name = file_name
        pixmap = QPixmap(file_name)
        self.label_image.setPixmap(pixmap)

    def sections_list_action_triggered(self):
        self.sections_window = section_screen.SectionsWindow()
        self.sections_window.move(self.pos())
        self.sections_window.resize(self.size())
        self.sections_window.show()
        self.close()
        #self.destroy()

    def redakt_action_triggered(self):
        self.redakt_window = redakt4.MainWindow()
        self.redakt_window.move(self.pos())
        self.redakt_window.resize(self.size())
        self.redakt_window.show()
        self.close()

    def edit_section_clicked(self):
        #print("edit section")
        s = self.button_create.text()
        if s != "Отправить изменения":
            self.button_create.setText("Отправить изменения")
            try:
                #print(self.line_input_head.text())
                if (self.image_file_name):
                    j = {
                        "isMain": True,
                        "title": str(self.line_input_head.text()),
                        "picture": redakt4.get_photo_uri(self.image_file_name),
                        "parentId": -1
                    }
                else:
                    j = {
                        "isMain": True,
                        "title": str(self.line_input_head.text()),
                        "picture": "",
                        "parentId": -1
                    }
                print(j)
                r = requests.post(global_constants.ARTICLE_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Ok!")
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка!")
                print(e)
            #self.status.showMessage("Раздел создан!")
        else:
            pass
            #self.status.showMessage("Изменения отправлены!")


if __name__ == '__main__':
    app = QApplication([])

    mw = SectionEditWindow()
    mw.show()

    app.exec()
