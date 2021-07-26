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
from PIL import Image

import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests

import redakt4
import faculties_screen, faculty_edit, contacts_screen, section_screen
import global_constants

class ContactEditorWindow(QMainWindow):
    def __init__(self, faculty_info=None,
                    contact_id=None, contact_name=None, contact_position=None, contact_number=None, 
                    photo_path = None, photo_url=None, contact_links=[]):
        QMainWindow.__init__(self)
        self.faculty_info = faculty_info
        if self.faculty_info:
            self.fac_id = self.faculty_info.fac_id
        else:
            self.fac_id = None

        self.contact_id = contact_id
        self.contact_name = contact_name
        self.contact_position = contact_position
        self.photo_path = photo_path
        self.photo_url = photo_url
        #print(photo_url)
        self.contact_number = contact_number
        self.contact_links = contact_links
        self.links_edits = []
        self.init_ui()
        self.init_menu()
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.resize(800, 450)

    def init_ui(self):
        main_main_layout = QVBoxLayout()

        main_layout = QHBoxLayout()
        self.setObjectName("MainWindow")
        
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName("centralwidget")
        #self.main_widget.setLayout(main_layout)
        self.main_widget.setLayout(main_main_layout)
        self.setCentralWidget(self.main_widget)

        self.labels_layout = QVBoxLayout()

        font_labels = QFont()
        font_labels.setPointSize(10)

        self.font_lines = QFont()
        self.font_lines.setPointSize(12)

        self.label_name = QtWidgets.QLabel()
        self.label_name.setObjectName("label_name")
        self.label_name.setFont(font_labels)

        self.lineEdit_name = QtWidgets.QLineEdit()
        self.lineEdit_name.setObjectName("lineEdit")
        self.lineEdit_name.setFont(self.font_lines)
        if self.contact_name:
            self.lineEdit_name.setText(self.contact_name)
        self.lineEdit_name.setCursorPosition(0)

        #group_layout = QHBoxLayout()
        #group_layout.setAlignment(Qt.AlignLeft)

        self.label_group = QLabel()
        self.label_group.setObjectName("label_group")
        self.label_group.setFont(font_labels)

        self.group_combobox = QComboBox()
        self.group_combobox_items = ["Дирекция", "Студсовет", "Другое"]
        self.group_combobox.addItems(self.group_combobox_items) 
        self.group_combobox.setFont(self.font_lines)
        #self.type_combobox.setCurrentIndex(self.fac_type)

        #group_layout.addWidget(self.label_group)
        #group_layout.addWidget(self.group_combobox)
        

        self.label_phone_number = QtWidgets.QLabel()
        self.label_phone_number.setObjectName("label_phone_number")
        self.label_phone_number.setFont(font_labels)

        self.lineEdit_phone_number = QtWidgets.QLineEdit()
        self.lineEdit_phone_number.setObjectName("lineEdit_phone_number")
        self.lineEdit_phone_number.setFont(self.font_lines)
        if self.contact_number:
            self.lineEdit_phone_number.setText(self.contact_number)
        self.lineEdit_phone_number.setCursorPosition(0)
        
        self.label_position = QtWidgets.QLabel()
        #self.label_position.setGeometry(QtCore.QRect(470, 170, 211, 16))
        self.label_position.setObjectName("label_position")
        self.label_position.setFont(font_labels)

        self.lineEdit_position = QtWidgets.QLineEdit()
        #self.lineEdit_position.setGeometry(QtCore.QRect(470, 200, 311, 21))
        self.lineEdit_position.setObjectName("lineEdit_position")
        self.lineEdit_position.setFont(self.font_lines)
        if self.contact_position:
            self.lineEdit_position.setText(self.contact_position)
        self.lineEdit_position.setCursorPosition(0)

        links_widget = QWidget()
        self.links_layout = QVBoxLayout()
        self.links_layout.setAlignment(Qt.AlignTop)
        self.labels_layout.setAlignment(Qt.AlignTop)
        links_widget.setLayout(self.links_layout)


        self.button_add = QtWidgets.QPushButton()
        self.button_add.setObjectName("button_add")
        self.button_add.setFont(font_labels)
        self.button_add.clicked.connect(self.add_link)
        
        self.label_links = QtWidgets.QLabel()
        #self.label_links.setGeometry(QtCore.QRect(470, 240, 231, 16))
        self.label_links.setObjectName("label_label_links")
        self.label_links.setFont(font_labels)
        
        if self.contact_links:
            for link in self.contact_links:
                lineEdit_link = QtWidgets.QLineEdit()
                lineEdit_link.setFont(self.font_lines)
                lineEdit_link.setText(link)
                self.links_edits.append(lineEdit_link)
                self.links_layout.addWidget(lineEdit_link)
        lineEdit_link = QtWidgets.QLineEdit()
        lineEdit_link.setFont(self.font_lines)
        self.links_edits.append(lineEdit_link)
        self.links_layout.addWidget(lineEdit_link)

        #self.links_layout.addWidget(self.lineEdit_first_link)
        self.links_layout.addWidget(self.button_add)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(links_widget)



        self.labels_layout.addWidget(self.label_name)
        self.labels_layout.addWidget(self.lineEdit_name)

        self.labels_layout.addWidget(self.label_group)
        self.labels_layout.addWidget(self.group_combobox)
        #self.labels_layout.addLayout(group_layout)

        self.labels_layout.addWidget(self.label_position)
        self.labels_layout.addWidget(self.lineEdit_position)

        self.labels_layout.addWidget(self.label_phone_number)
        self.labels_layout.addWidget(self.lineEdit_phone_number)

        self.labels_layout.addWidget(self.label_links)
        self.labels_layout.addWidget(self.scroll)
        #self.labels_layout.addWidget(self.lineEdit_first_link)
        #self.labels_layout.addWidget(self.button_add)

        self.labels_layout.setAlignment(Qt.AlignTop)
        

        self.attachment_layout = QVBoxLayout()

        self.button_font = QFont()
        self.button_font.setPointSize(10)

        self.label_image = QtWidgets.QLabel()
        #self.label_image.setGeometry(QtCore.QRect(96, 92, 131, 61))
        #self.label_image.setText("")
        self.label_size = 180
        self.maximum_height = self.label_size + 100
        if self.photo_path:
            pixmap = QPixmap(self.photo_path).scaled(self.label_size, self.maximum_height, Qt.KeepAspectRatio)    
        else:
            pixmap = QPixmap("images/attach.png").scaled(self.label_size, self.maximum_height, Qt.KeepAspectRatio)
        #pixmap.scaledToWidth(label_size)
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)
        self.label_image.setMaximumWidth(self.label_size)
        #self.label_image.setMaximumHeight(label_size)
        #self.label_image.setMinimumWidth(self.label_size)
        #self.label_image.setMinimumHeight(label_size)
        self.label_image.setObjectName("label_image")

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.setFont(self.button_font)
        self.button_open.clicked.connect(self._on_open_image)
        self.button_open.setMaximumWidth(self.label_size)
        #self.button_open.setGeometry(QtCore.QRect(70, 10, 211, 31))
        self.button_open.setObjectName("button_open")

        self.button_edit = QPushButton()
        self.button_edit.setText("Создать контакт")
        if self.contact_id:
            self.button_edit.setText("Отправить изменения")
        #self.button_edit.setFont(self.button_font)
        self.button_edit.setFont(self.font_lines)
        #self.button_edit.setMaximumWidth(self.label_size)
        self.button_edit.clicked.connect(self.edit_contact)

        self.labels_layout.addWidget(self.button_edit)


        self.attachment_layout.addWidget(self.label_image)
        self.attachment_layout.addWidget(self.button_open)
        #self.attachment_layout.addWidget(self.button_edit)
        self.attachment_layout.setAlignment(Qt.AlignTop)

        if self.contact_id:
            self.add_delete_button()


        main_layout.addLayout(self.attachment_layout)
        main_layout.addLayout(self.labels_layout)

        navigation_font = QFont()
        navigation_font.setPointSize(12)

        navigation_layout = QHBoxLayout()
        self.button_back = QPushButton()
        self.button_back.setText("<")
        self.button_back.setMaximumWidth(30)
        self.button_back.setFont(navigation_font)
        #self.button_back.clicked.connect(self.faculties_list_action_triggered)
        self.button_back.clicked.connect(self.back_to_contacts)

        navigation_label = QLabel()
        navigation_label.setText("Структурные подразделения/Редактирование СП/Редактирование контакта")
        navigation_label.setFont(navigation_font)

        navigation_layout.addWidget(self.button_back)
        navigation_layout.addWidget(navigation_label)
        navigation_layout.setAlignment(Qt.AlignTop)

        
        main_main_layout.setAlignment(Qt.AlignTop)
        main_main_layout.addLayout(navigation_layout)
        main_main_layout.addLayout(main_layout)
        

        #self.menubar = QtWidgets.QMenuBar(self)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        #self.menubar.setObjectName("menubar")
        #self.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(self)
        #self.statusbar.setObjectName("statusbar")
        #self.setStatusBar(self.statusbar)

        #self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

           
    def _on_open_image(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "<Прикрепите фото контакта>" ,None,"Image(*.png *jpg)")[0]  
        if not file_name:
            return
        self.photo_path = file_name
        self.photo_url = None
        background = QPixmap(file_name).scaled(self.label_size, self.maximum_height, Qt.KeepAspectRatio) 
        #pixmap = QPixmap(file_name)
        self.label_image.setPixmap(background)

    def add_link(self):
        lineEdit_link = QtWidgets.QLineEdit()
        lineEdit_link.setFont(self.font_lines)
        self.links_edits.append(lineEdit_link)
        self.links_layout.insertWidget(self.links_layout.count()-1, lineEdit_link)

    
    def add_delete_button(self):
        self.button_delete = QPushButton("Удалить контакт")
        #self.button_delete.setText("Удалить")
        #font = QFont()
        #font.setPointSize(9)
        #self.button_delete.setFont(font)
        self.button_delete.setFont(self.button_font)
        self.button_delete.setIcon(QIcon("images/bin.png"))
        self.button_delete.setIconSize(QSize(20,20))
        #self.button_delete.setMaximumWidth(175)
        self.button_delete.clicked.connect(self.delete_contact)
        
        #self.attachment_layout.insertWidget(self.attachment_layout.count()-1, self.button_delete)
        self.attachment_layout.addWidget(self.button_delete)
        #self.attachment_layout.addStretch()


    def add_faculty_clicked(self):
        #print("clicked!")
        self.faculty_edit_window = faculty_edit.FacultyEditWindow()
        self.faculty_edit_window.move(self.pos())
        self.faculty_edit_window.resize(self.size())
        self.faculty_edit_window.show()
        self.close()
        #self.destroy()


    def switch_to_sbornic(self):
        self.sbornic_screen = section_screen.SectionsWindow()
        self.sbornic_screen.move(self.pos())
        self.sbornic_screen.resize(self.size())
        self.sbornic_screen.show()
        self.close()


    def faculties_list_action_triggered(self):
        self.faculties_window = faculties_screen.FacultiesWindow()
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()


    def back_to_contacts(self):
        if self.fac_id is None:
            return
        self.button_back.setEnabled(False)
        self.contacts_window = contacts_screen.ContactsWindow(faculty_info=self.faculty_info)
        self.contacts_window.move(self.pos())
        self.contacts_window.resize(self.size())
        self.contacts_window.show()
        self.close()


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


    def delete_contact(self):
        if self.contact_id is None:
            return
        #payload = {'id': self.sect_id}
        try:
            r = requests.delete(global_constants.CONTACTS_API+f"/{self.contact_id}")
            if (r.status_code == 200):
                self.status.showMessage("Контакт удалён!")
                self.back_to_contacts()
            else:
                self.status.showMessage("Ошибка при удалении.")
                print(r.status_code)
        except Exception as e:
            #self.print(e.messa)
            self.status.showMessage("Ошибка при отправке запроса!")

    
    def get_links(self):
        links = []
        for linkEdit in self.links_edits:
            text = linkEdit.text()
            if (text is not None) and len(text)>0:
                links.append(text)
        return links


    def edit_contact(self):
        #print("edit section")
        #s = self.button_create.text()
        if self.contact_id is None:
            self.button_edit.setText("Отправить изменения")
            try:
                #print(self.line_input_head.text())
                j = {
                        "facultyId": self.fac_id,
                        "name": self.lineEdit_name.text(),
                        "position": self.lineEdit_position.text(),
                        "phoneNumber": self.lineEdit_phone_number.text(),
                        "links": self.get_links(),
                        "photo": ""
                    }
                if (self.photo_path):
                    self.photo_url = redakt4.get_photo_uri(self.photo_path)
                    j["photo"] = self.photo_url
                #print(j)
                r = requests.post(global_constants.CONTACTS_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Контакт создан!")
                    #print(r.json())
                    self.contact_id = r.json()['id']
                    self.contact_name = r.json()['name']
                    self.add_delete_button()
                else:
                    print(r.status_code)
            except Exception as e:
                #import traceback
                self.status.showMessage("Ошибка!")
                #print(traceback.format_exc())
            #self.status.showMessage("Раздел создан!")
        else:
            j = {
                    "id": self.contact_id,
                    "facultyId": self.fac_id,
                    "name": self.lineEdit_name.text(),
                    "position": self.lineEdit_position.text(),
                    "phoneNumber": self.lineEdit_phone_number.text(),
                    "links": self.get_links(),
                    "photo": ""
                }
            if self.photo_url:
                j["photo"] = self.photo_url
            else:
                if (self.photo_path):
                    try:
                        self.photo_url = redakt4.get_photo_uri(self.photo_path)
                        j["photo"] = self.photo_url
                    except Exception as e:
                        print(e)
                else:
                    pass
            try:
                r = requests.put(global_constants.CONTACTS_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Изменения отправлены!")
                    #print(r.json())
                    self.contact_id = r.json()['id']
                    self.contact_name = r.json()['name']
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка при отправке!")
            #print("section exists")


    def init_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        self.menu_screens = QtWidgets.QMenu(self.menubar)
        self.menu_screens.setObjectName("menuscreens")
        
        self.menu_modes = QtWidgets.QMenu(self.menubar)
        self.menu_modes.setObjectName("menumodes")
        
        self.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(self)
        #self.statusbar.setObjectName("statusbar")
        #self.setStatusBar(self.statusbar)

        self.faculties_list_action = QtWidgets.QAction(self)
        self.faculties_list_action.setObjectName("sectionslistaction")
        self.faculties_list_action.triggered.connect(self.faculties_list_action_triggered)
        
        self.faculty_creation = QtWidgets.QAction(self)
        self.faculty_creation.setObjectName("action_2")
        self.faculty_creation.triggered.connect(self.add_faculty_clicked)

        self.contacts_action = QtWidgets.QAction(self)
        self.contacts_action.setObjectName("contacts_action")
        self.contacts_action.triggered.connect(self.back_to_contacts)

        #self.article_creation = QtWidgets.QAction(self)
        #self.article_creation.setObjectName("action_3")
        #self.article_creation.triggered.connect(self.redakt_action_triggered)
        
        self.sbornic_action = QtWidgets.QAction(self)
        self.sbornic_action.setObjectName("action_4")
        self.sbornic_action.triggered.connect(self.switch_to_sbornic)
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        
        self.menu_screens.addAction(self.faculties_list_action)
        self.menu_screens.addAction(self.faculty_creation)
        self.menu_screens.addAction(self.contacts_action)
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        #self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "ИСП admin"))
        self.label_name.setText(_translate("MainWindow", "Имя контакта:"))
        self.label_group.setText(_translate("MainWindow", "Группа контакта:"))
        self.label_phone_number.setText(_translate("MainWindow", "Телефон контакта:"))
        self.label_position.setText(_translate("MainWindow", "Должность контакта:"))
        #self.attach_button.setText(_translate("MainWindow", "<Прикрепите фото контакта>"))
        #self.pushButton.clicked.connect(self._on_open_image)
        self.button_add.setText(_translate("MainWindow", "+"))
        self.label_links.setText(_translate("MainWindow", "Ссылки:"))
        #self.setWindowTitle(_translate("MainWindow", "Редактирование раздела"))
        self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.faculties_list_action.setText(_translate("MainWindow", "Список факультетов"))
        self.faculty_creation.setText(_translate("MainWindow", "Создание факультета"))
        self.contacts_action.setText(_translate("MainWindow", "Контакты факультета"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    contactEditWindow = ContactEditorWindow()
    contactEditWindow.show()
    sys.exit(app.exec_())
