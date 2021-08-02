#from faculties_screen import FacultiesWindow
from PyQt5 import QtCore, QtGui, QtWidgets
#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *

from quamash import QEventLoop

import global_constants
import requests
from authorization_api import AuthorizationApi
from authorization_api import UserApi, UserData
from login_screen import LoginWindow
from add_user_screen import EditUserWindow
from preloader import Preloader
import asyncio, aiohttp
import section_screen
import faculties_screen

class User(QFrame):
    def __init__(self, user_data=None, admin_window=None):
        QFrame.__init__(self)
        self.user_login = user_data.login
        self.user_role = user_data.role
        self.admin_window = admin_window
        self.init_ui()

    def init_ui(self, icon_png="images/user.png"):
        self.setFrameShape(QFrame.Box)
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        label_font = QFont()
        label_font.setPointSize(12)

        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignLeft)

        login_label = QLabel(self)
        login_label.setText(self.user_login)
        login_label.setFont(label_font)


        #role_label = QLabel(self)
        #role_label.setText(self.user_role)
        user_icon_label = QLabel(self)
        user_icon_label.setScaledContents(True)
        icon_pixmap = QPixmap(icon_png).scaled(30,30)
        user_icon_label.setPixmap(icon_pixmap)

        #button_edit_login = QPushButton(self)
        #button_edit_login.setIcon(QIcon(icon_png))
        #button_edit_login.setMaximumWidth(50)
        #button_edit_login.setEnabled(False)

        login_layout.addWidget(user_icon_label)
        login_layout.addWidget(login_label)
        #login_layout.addWidget(button_edit_login)
        #login_layout.addWidget(user_icon_label)

        self.button_edit_password = QPushButton(self)
        self.button_edit_password.setText("Сменить пароль")
        self.button_edit_password.setFont(label_font)
        self.button_edit_password.clicked.connect(self.change_password)

        self.button_delete = QPushButton(self)
        self.button_delete.setIcon(QIcon("images/bin.png"))
        self.button_delete.setMaximumWidth(60)
        self.button_delete.clicked.connect(self.delete_clicked)

        #layout.addWidget(login_label)
        #layout.addWidget(button_edit_login)
        layout.addLayout(login_layout)
        layout.addWidget(self.button_edit_password)
        layout.addWidget(self.button_delete)
        #button_edit_login.setText("Изменить логин")
    
    def delete_clicked(self):
        self.admin_window.delete_admin(self.user_login, self)
        self.setEnabled(False)

    def change_password(self):
        self.admin_window.edit_admin_clicked(self.user_login)


class AdminWindow(QMainWindow):
    def __init__(self, authorization_api=AuthorizationApi(), previousWindow=None):
        QMainWindow.__init__(self)
        self.setWindowTitle("ИСП админ")
        self.authorization_api = authorization_api
        self.previousWindow = previousWindow
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.resize(800, 600)
        self.admins_inited = False
        self.init_ui()
        self.init_menu()


    def showEvent(self, event):
        token = self.authorization_api.get_token()
        stop_condition = False
        if token is None:
            self.login_window = LoginWindow(self.authorization_api, parent=self)
            if self.login_window.exec_() == QDialog.Accepted:
                token = self.authorization_api.get_token()
            else:
                self.status.showMessage("Необходимо иметь права админа для отправки")
                stop_condition = True
        self.user_api = UserApi(token=token)
        if stop_condition:
            asyncio.ensure_future(self.stop_admin_window())
        else:
            if not self.admins_inited:
                asyncio.ensure_future(self.init_admins())


    async def stop_admin_window(self):
        loop = asyncio.get_event_loop()
        await asyncio.sleep(0.1, loop=loop)
        if self.previousWindow:
            self.previousWindow.show()
        self.close()
    

    def init_ui(self):
        widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        widget.setLayout(self.scroll_layout)


        self.preloader = Preloader()
        self.scroll_layout.addWidget(self.preloader)
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
        self.head_label.setText("Администраторы")
        #self.head_label.setMinimumHeight(50)
        #self.head_label.setMinimumWidth(100)
        #self.head_label.setMaximumWidth(300)
        #self.head_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.add_admin_button = QPushButton("+")
        self.add_admin_button.setFont(font)
        self.add_admin_button.setMaximumWidth(100)
        self.add_admin_button.clicked.connect(self.add_admin_clicked)
        #self.add_admin_button.clicked.connect(self.add_faculty_clicked)

        head_layout.addWidget(self.head_label)
        head_layout.addWidget(self.add_admin_button)


        main_layout = QVBoxLayout()
        main_layout.addLayout(head_layout)
        #main_layout.addWidget(self.head_label)
        #main_layout.addWidget(self.head_widget)
        main_layout.addWidget(self.scroller)
        
        #main_layout.addStretch()
        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)


    async def init_admins(self):
        #print("init sections")
        self.usersData = await self.user_api.get_users()

        users = []
        for userData in self.usersData:
            user = User(user_data=userData, admin_window=self)
            users.append(user)
        
        self.preloader.stop_loader_animation()
        self.scroll_layout.removeWidget(self.preloader)
        self.preloader.hide()
        self.scroll_layout.setAlignment(Qt.AlignTop)

        for user in users:
            #section.clicked.connect(lambda: section.edit_clicked(self))
            self.scroll_layout.addWidget(user)

        #self.scroll_layout.addStretch()
        self.admins_inited = True


    def edit_admin_clicked(self, admin_login):
        if self.admins_inited:
            self.edit_user_window = EditUserWindow(self.authorization_api, admin_login, parent=self)
            if self.edit_user_window.exec_() == QDialog.Accepted:
                self.admins_inited = False
                for i in reversed(range(self.scroll_layout.count())):
                    item = self.scroll_layout.itemAt(i)
                    widget = item.widget()
                    widget.setParent(None)
                self.scroll_layout.setAlignment(Qt.AlignVCenter)
                self.preloader.show()
                self.preloader.start_loader_animation()
                asyncio.ensure_future(self.init_admins())


    def add_admin_clicked(self):
        if self.admins_inited:
            self.edit_user_window = EditUserWindow(self.authorization_api, None, parent=self)
            if self.edit_user_window.exec_() == QDialog.Accepted:
                self.admins_inited = False
                for i in reversed(range(self.scroll_layout.count())):
                    item = self.scroll_layout.itemAt(i)
                    widget = item.widget()
                    widget.setParent(None)
                self.scroll_layout.setAlignment(Qt.AlignVCenter)
                self.preloader.show()
                self.preloader.start_loader_animation()
                asyncio.ensure_future(self.init_admins())


    def delete_admin(self, admin_login, user_widget):
        if admin_login:
            token = self.authorization_api.get_token()
            if token is None:
                self.status.showMessage("Необходимо иметь права админа для удаления")
                return
            headers = {"Authorization": "Bearer "+token}
            try:
                r = requests.delete(global_constants.USER_API+f"/{admin_login}", headers=headers)
                if r.status_code == 200:
                    self.scroll_layout.removeWidget(user_widget)
                    user_widget.setParent(None)
                    self.status.showMessage("Пользователь успешно удалён")
                else:
                    self.status.showMessage("Ошибка при удалении пользователя!")
                    user_widget.setEnabled(True)
            except Exception as e:
                self.status.showMessage("Ошибка при удалении пользователя!")
        else:
            self.setEnabled(True)

            

    def switch_to_sbornic(self):
        self.sbornic_screen = section_screen.SectionsWindow(authorization_api=self.authorization_api)
        self.sbornic_screen.move(self.pos())
        self.sbornic_screen.resize(self.size())
        self.sbornic_screen.show()
        self.close()

    
    def switch_to_faculty(self):
        self.faculties_window = faculties_screen.FacultiesWindow(authorization_api=self.authorization_api)
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()


    def init_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        self.menu_modes = QtWidgets.QMenu(self.menubar)
        self.menu_modes.setObjectName("menumodes")
        
        self.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(self)
        #self.statusbar.setObjectName("statusbar")
        #self.setStatusBar(self.statusbar)

        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        self.sbornic_action.triggered.connect(self.switch_to_sbornic)
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        self.faculty_action.triggered.connect(self.switch_to_faculty)

        self.admins_action = QtWidgets.QAction(self)
        self.admins_action.setObjectName("action_6")
        
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        self.menu_modes.addAction(self.admins_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        #self.setWindowTitle(_translate("ScrollArea", "ИСП admin"))
        #self.setWindowTitle(_translate("MainWindow", "Редактирование раздела"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))
        self.admins_action.setText(_translate("MainWindow", "Админ-панель"))
        
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    authorization_api = AuthorizationApi()
    admin_window = AdminWindow(authorization_api=authorization_api, previousWindow=faculties_screen.FacultiesWindow(authorization_api=authorization_api))
    admin_window.show()

    with loop:
        #print("loop")
        loop.run_forever()