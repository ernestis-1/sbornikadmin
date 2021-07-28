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

class EditUserWindow(QDialog):
    def __init__(self, authorization_api=None, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Создание пользователя")
        self.authorization_api = authorization_api
        self.next_window = parent
        self.remember_me = False
        self.login_after_creation = False
        self.resize(500, 300)
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
        self.label_head.setText("Создание пользователя") 
        self.label_head.setAlignment(Qt.AlignHCenter)

        self.label_login = QLabel()
        self.label_login.setText("Логин")
        self.label_login.setFont(self.labels_font)

        self.login_input = QLineEdit()
        self.login_input.setFont(self.input_font)

        self.label_password = QLabel()
        self.label_password.setText("Пароль")
        self.label_password.setFont(self.labels_font)

        self.password_input = QLineEdit()
        self.password_input.setFont(self.input_font)

        self.label_password_confirmation = QLabel()
        self.label_password_confirmation.setText("Подтверждение пароля")
        self.label_password_confirmation.setFont(self.labels_font)

        self.password_confirmation_input = QLineEdit()
        self.password_confirmation_input.setFont(self.input_font)


        self.checkbox_layout = QHBoxLayout()

        self.login_after_creation_checkbox = QCheckBox()
        self.login_after_creation_checkbox.setText("Войти после создания")
        self.login_after_creation_checkbox.setFont(self.labels_font)
        self.login_after_creation_checkbox.stateChanged.connect(self.login_after_creation_changed)

        self.remember_me_checkbox = QCheckBox()
        self.remember_me_checkbox.setText("Запомнить меня")
        self.remember_me_checkbox.setFont(self.labels_font)
        self.remember_me_checkbox.stateChanged.connect(self.remember_me_changed)
        self.remember_me_checkbox.setEnabled(False)

        self.checkbox_layout.addWidget(self.login_after_creation_checkbox)
        self.checkbox_layout.addWidget(self.remember_me_checkbox)


        self.button_create = QPushButton()
        self.button_create.setText("Создать")
        self.button_create.setFont(self.head_font)
        self.button_create.clicked.connect(self.create_clicked)

        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.label_head)
        main_layout.addWidget(self.label_login)
        main_layout.addWidget(self.login_input)
        main_layout.addWidget(self.label_password)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.label_password_confirmation)
        main_layout.addWidget(self.password_confirmation_input)
        main_layout.addLayout(self.checkbox_layout)
        #main_layout.addWidget(QLabel())
        main_layout.addWidget(self.button_create)


    def remember_me_changed(self, state):
        self.remember_me = state == Qt.Checked

    def login_after_creation_changed(self, state):
        self.login_after_creation = state == Qt.Checked
        if self.login_after_creation:
            self.remember_me_checkbox.setEnabled(True)
        else:
            self.remember_me_checkbox.setEnabled(False)


    def create_clicked(self):
        login = str(self.login_input.text())
        password = str(self.password_input.text())
        password_confirmation = str(self.password_confirmation_input.text())
        if (password != password_confirmation):
            self.password_input.clear()
            self.password_confirmation_input.clear()
            self.label_head.setText("Пароль не совпадает с подтверждением")
            return
        if login == "" or login is None or password == "" or password is None:
            self.password_input.clear()
            self.password_confirmation_input.clear()
            self.label_head.setText("Логин и пароль не могут быть пустыми")
            return
        token = self.authorization_api.get_token()
        if token:  
            headers = {"Authorization": "Bearer "+token}
            j = {
                "login": login,
                "password": password,
                "role": "User"
            }
            try:
                r = requests.post(global_constants.USER_API, json=j, headers=headers)
                if r.status_code == 200:
                    if self.login_after_creation:
                        self.authorization_api.init_api(remember_me=self.remember_me, login=login, password=password)
                    self.accept()
                else:
                    self.label_head.setText("Произошла ошибка при отправке запроса.(Код"+str(r.status_code)+")")
            except Exception as e:
                self.label_head.setText("Произошла ошибка при отправке запроса.")
        else:
            self.login_input.clear()
            self.password_input.clear()
            self.password_confirmation_input.clear()
            self.label_head.setText("Ошибка! Необходимо иметь права админа")

    def closeEvent(self, event):
        self.reject()
        #if self.next_window:
            #self.next_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = EditUserWindow(AuthorizationApi())
    loginWindow.show()
    sys.exit(app.exec_())