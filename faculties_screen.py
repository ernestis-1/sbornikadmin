# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scroll.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
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

from quamash import QEventLoop

import aiohttp, asyncio

from preloader import Preloader
from faculty_api import FacultiesApi, BaseFacultyInfo
import faculty_edit
import global_constants
import section_screen
import admin_panel
from authorization_api import AuthorizationApi


class Faculty(QPushButton):
    def __init__(self, faculty_info=None, img_path="images/building.png", facultiesWindow=None):
        QPushButton.__init__(self)
        self.faculty_info = faculty_info
        self.fac_id = faculty_info.fac_id
        self.fac_name = faculty_info.fac_name
        self.info = faculty_info.info
        self.img_url = faculty_info.img_url
        self.facultiesWindow = facultiesWindow
        self.init_ui(img_path)
        self.clicked.connect(self.edit_clicked)

    def init_ui(self, img_path):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setMaximumHeight(150)
        self.setMinimumHeight(140)

        label = QtWidgets.QLabel(self)
        #self.label.setGeometry(QtCore.QRect(40, 50, 151, 141))
        label.setMaximumHeight(120)
        label.setMaximumWidth(120)
        label.setPixmap(QtGui.QPixmap(img_path))
        label.setScaledContents(True)
        label.setObjectName("label")
        #layout.addWidget(label)
        #layout.addStretch(0)
        #layout.setAlignment(Qt.AlignLeft)

        label_2 = QtWidgets.QLabel(self)
        #self.label_2.setGeometry(QtCore.QRect(220, 60, 241, 101))
        label_2.setMinimumHeight(120)
        font = QFont()
        font.setPointSize(14)
        label_2.setFont(font)
        label_2.setText(self.fac_name)
        label_2.setAutoFillBackground(False)
        label_2.setWordWrap(True)
        label_2.setTextFormat(QtCore.Qt.AutoText)
        label_2.setScaledContents(False)
        label_2.setObjectName("label_2")
        label_2.setMargin(10)


        layout.addWidget(label_2)
        layout.addStretch()
        layout.addWidget(label)

    
    def edit_clicked(self):
        #print("edit clicked")
        self.setEnabled(False)
        self.facultiesWindow.switch_to_edit_faculty(self.faculty_info)
        


class FacultiesWindow(QMainWindow):
    def __init__(self, authorization_api=AuthorizationApi()):
        QMainWindow.__init__(self)
        self.authorization_api = authorization_api
        self.resize(800, 600)
        self.api = FacultiesApi(global_constants.FACULTIES_API, global_constants.FACULTIES_INFO_API, global_constants.FACULTIES_INFO_ID,
            global_constants.CONTACT_TYPES_API, global_constants.FACULTIES_TYPES_API)
        self.faculties_inited = False
        self.faculty_types = None
        self.init_ui()
        self.init_menu()


    def init_ui(self):
        widget = QWidget()
        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)


        self.preloader = Preloader()
        self.layout.addWidget(self.preloader)
        #self.layout.addWidget(Faculty(fac_name="Институт Механики, Математики и Компьютерных Наук"))
        #self.layout.addWidget(Faculty(fac_name="Мехмат"))

        self.scroller = QScrollArea()
        #self.setCentralWidget(self.scroller)
        #self.scroller.setFixedWidth(650)
        self.scroller.setMinimumHeight(150)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        
        self.scroller.setWidget(widget)
        #self.scroller.adjustSize()

        head_layout = QHBoxLayout()
        #self.head_widget = QWidget()
        #self.head_widget.setFixedWidth(662)
        #self.head_widget.setLayout(head_layout)

        font = QtGui.QFont()
        font.setPointSize(14)

        self.head_label = QLabel()
        self.head_label.setFont(font)
        self.head_label.setText("Структурные подразделения")
        #self.head_label.setMinimumHeight(50)
        #self.head_label.setMinimumWidth(100)
        #self.head_label.setMaximumWidth(300)
        #self.head_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.add_section_button = QPushButton("+")
        self.add_section_button.setFont(font)
        self.add_section_button.setMaximumWidth(100)
        self.add_section_button.clicked.connect(self.add_faculty_clicked)

        head_layout.addWidget(self.head_label)
        head_layout.addWidget(self.add_section_button)


        main_layout = QVBoxLayout()
        main_layout.addLayout(head_layout)
        #main_layout.addWidget(self.head_label)
        #main_layout.addWidget(self.head_widget)
        main_layout.addWidget(self.scroller)
        
        #main_layout.addStretch()
        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)


    def showEvent(self, event):
        #print("show event")
        if not self.faculties_inited:
            asyncio.ensure_future(self.init_faculties())


    async def init_faculties(self):
        #print("init sections")
        self.faculties = await self.api.get_faculties()
        self.faculty_types = await self.api.get_faculties_types()

        faculties = []
        async with aiohttp.ClientSession() as session:
            for fac in self.faculties:
                faculty = Faculty(faculty_info=fac, facultiesWindow=self)
                faculties.append(faculty)
                #self.layout.addWidget(section)
        
        self.preloader.stop_loader_animation()
        self.layout.removeWidget(self.preloader)
        self.preloader.hide()

        for faculty in faculties:
            #section.clicked.connect(lambda: section.edit_clicked(self))
            self.layout.addWidget(faculty)

        self.layout.addStretch()
        self.faculties_inited = True


    def add_faculty_clicked(self):
        #print("clicked!")
        self.faculty_edit_window = faculty_edit.FacultyEditWindow(faculty_types=self.faculty_types,authorization_api=self.authorization_api)
        self.add_section_button.setEnabled(False)
        self.faculty_edit_window.move(self.pos())
        self.faculty_edit_window.resize(self.size())
        #self.faculty_edit_window.show()
        if self.isMaximized():
            self.faculty_edit_window.showMaximized()
        else:
            self.faculty_edit_window.show()
        self.close()
        #self.destroy()


    def switch_to_edit_faculty(self, faculty_info):
        #self.section_edit_window = faculty_edit.FacultyEditWindow(fac_id=fact_id, fac_name=fac_name, fac_info=fac_info, img_url=img_url)
        self.faculty_edit_window = faculty_edit.FacultyEditWindow(faculty_info, faculty_types=self.faculty_types, authorization_api=self.authorization_api)
        self.faculty_edit_window.move(self.pos())
        self.faculty_edit_window.resize(self.size())
        #self.faculty_edit_window.show()
        if self.isMaximized():
            self.faculty_edit_window.showMaximized()
        else:
            self.faculty_edit_window.show()
        self.close()


    def switch_to_sbornic(self):
        self.sbornic_screen = section_screen.SectionsWindow(authorization_api=self.authorization_api)
        self.sbornic_screen.move(self.pos())
        self.sbornic_screen.resize(self.size())
        #self.sbornic_screen.show()
        if self.isMaximized():
            self.sbornic_screen.showMaximized()
        else:
            self.sbornic_screen.show()
        self.close()


    def switch_to_admins(self):
        self.admins_screen = admin_panel.AdminWindow(authorization_api=self.authorization_api, previousWindow=self)
        self.admins_screen.move(self.pos())
        self.admins_screen.resize(self.size())
        #self.admins_screen.show()
        if self.isMaximized():
            self.admins_screen.showMaximized()
        else:
            self.admins_screen.show()
        self.close()


    def init_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        #self.menu_screens = QtWidgets.QMenu(self.menubar)
        #self.menu_screens.setObjectName("menuscreens")
        
        self.menu_modes = QtWidgets.QMenu(self.menubar)
        self.menu_modes.setObjectName("menumodes")
        
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        
        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        self.sbornic_action.triggered.connect(self.switch_to_sbornic)
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")

        self.admins_action = QtWidgets.QAction(self)
        self.admins_action.setObjectName("action_6")
        self.admins_action.triggered.connect(self.switch_to_admins)


        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        self.menu_modes.addAction(self.admins_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        #self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ScrollArea", "ИСП admin"))
        #self.setWindowTitle(_translate("MainWindow", "Редактирование раздела"))
        #self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        #self.sections_list_action.setText(_translate("MainWindow", "Список разделов"))
        #self.faculty_creation.setText(_translate("MainWindow", "Создание факультета"))
        #self.article_creation.setText(_translate("MainWindow", "Создание статьи"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))
        self.admins_action.setText(_translate("MainWindow", "Админ-панель"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    authorization_api = AuthorizationApi()
    facultiesWindow = FacultiesWindow(authorization_api=authorization_api)
    facultiesWindow.show()

    with loop:
        #print("loop")
        loop.run_forever()
    #sys.exit(app.exec_())
