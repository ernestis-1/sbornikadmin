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

import global_constants
import requests
from authorization_api import AuthorizationApi

class LoginWindow(QDialog):
    def __init__(self, authorization_api=None, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Авторизация")
        self.authorization_api = authorization_api
        self.next_window = parent
        self.remember_me = False
        self.resize(500, 250)
        self.init_ui()
        

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        #main_layout = QVBoxLayout()
        #self.main_widget = QWidget()
        #self.main_widget.setLayout(main_layout)
        #self.setCentralWidget(self.main_widget)
        
        self.labels_font = QFont()
        self.labels_font.setPointSize(10)
        self.input_font = QFont()
        self.input_font.setPointSize(12)
        self.head_font = QFont()
        self.head_font.setPointSize(14)

        self.label_head = QLabel()
        self.label_head.setFont(self.head_font)
        self.label_head.setText("Вход в аккаунт администратора") 
        self.label_head.setAlignment(Qt.AlignHCenter)

        self.label_login = QLabel()
        self.label_login.setText("username")
        self.label_login.setFont(self.labels_font)

        self.login_input = QLineEdit()
        self.login_input.setFont(self.input_font)

        self.label_password = QLabel()
        self.label_password.setText("password")
        self.label_password.setFont(self.labels_font)

        self.password_input = QLineEdit()
        self.password_input.setFont(self.input_font)


        self.remember_me_checkbox = QCheckBox()
        self.remember_me_checkbox.setText("Запомнить меня")
        self.remember_me_checkbox.setFont(self.labels_font)
        #self.remember_me_checkbox.toggle()
        self.remember_me_checkbox.stateChanged.connect(self.remember_me_changed)


        self.button_login = QPushButton()
        self.button_login.setText("Войти")
        self.button_login.setFont(self.head_font)
        self.button_login.clicked.connect(self.login_clicked)

        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.label_head)
        main_layout.addWidget(self.label_login)
        main_layout.addWidget(self.login_input)
        main_layout.addWidget(self.label_password)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.remember_me_checkbox)
        #main_layout.addWidget(QLabel())
        main_layout.addWidget(self.button_login)


    def remember_me_changed(self, state):
        self.remember_me = state == Qt.Checked

    def login_clicked(self):
        login = str(self.login_input.text())
        password = str(self.password_input.text())
        self.authorization_api.init_api(remember_me=self.remember_me, login=login, password=password)
        #print(self.authorization_api.get_token())
        self.accept()

    def closeEvent(self, event):
        self.reject()
        #if self.next_window:
            #self.next_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = LoginWindow(AuthorizationApi())
    loginWindow.show()
    sys.exit(app.exec_())