from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import (QWidget, QGridLayout,
    QPushButton, QApplication)

from quamash import QEventLoop

import aiohttp, asyncio

from preloader import Preloader
from faculty_api import FacultiesApi, BaseFacultyInfo , GatherImages
from sections_api import get_image_path_from_url
import faculty_edit
import faculties_screen
import global_constants
import section_screen, admin_panel
import contact_edit
from authorization_api import AuthorizationApi

class Contact(QPushButton):
    def __init__(self, contact_id=None, contact_name=None, contact_position=None, photo_url=None, 
                    photo_path="images/attach.png", contact_number=None,
            contact_links=None, contacts_window=None):
        QWidget.__init__(self)
        self.contact_id = contact_id
        self.contact_name = contact_name
        self.contact_position = contact_position
        self.contact_number = contact_number
        self.contact_links = contact_links
        self.photo_url = photo_url
        self.photo_path = photo_path
        self.contacts_window = contacts_window
        self.init_ui()
        self.clicked.connect(self.edit_clicked)

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self.setMaximumHeight(160)
        self.setMinimumHeight(130)

        self.label_image = QLabel(self)
        image_width = 100
        image_max_height = 140

        self.label_image.setMaximumHeight(image_max_height)
        self.label_image.setMaximumWidth(image_width)
        self.label_image.setMinimumWidth(image_width)
        pixmap = QPixmap(self.photo_path).scaled(image_width, image_max_height, Qt.KeepAspectRatio)
        #pixmap.scaledToWidth(label_size)
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)
        
        main_layout.addWidget(self.label_image)

        info_font = QFont()
        info_font.setPointSize(12)
        self.label_name = QLabel(self)
        self.label_name.setText(self.contact_name)
        self.label_name.setFont(info_font)

        self.label_position = QLabel(self)
        self.label_position.setText(self.contact_position)
        self.label_position.setFont(info_font)

        info_layout = QVBoxLayout()


        info_layout.addWidget(self.label_name)
        info_layout.addWidget(self.label_position)
        info_layout.setContentsMargins(20,0,0,0)
        
        main_layout.addWidget(self.label_image)
        main_layout.addLayout(info_layout)

    def edit_clicked(self):
        if self.contacts_window:
            self.setEnabled(False)
            self.contacts_window.forbidDeletion(self.photo_path)
            self.contacts_window.open_contact_edit(self.contact_id, self.contact_name, self.contact_position, self.contact_number,
                self.photo_path, self.photo_url, self.contact_links)


class ContactsWindow(QMainWindow):
    def __init__(self, faculty_info=None, authorization_api=AuthorizationApi()):
        QMainWindow.__init__(self)
        self.resize(800,600)
        self.authorization_api = authorization_api
        self.faculty_info = faculty_info
        if self.faculty_info:
            self.fac_id = faculty_info.fac_id
            self.fac_name = faculty_info.fac_name
            self.fac_info = faculty_info.info
            self.fac_img_url = faculty_info.img_url
        else:
            self.fac_id = None
            self.fac_name = None
            self.fac_info = None
            self.fac_img_url = None
        self.contacts_inited = False
        self.api = FacultiesApi(global_constants.FACULTIES_API, global_constants.FACULTIES_INFO_API, global_constants.FACULTIES_INFO_ID)
        self.setWindowTitle("Контакты")
        self.init_ui()
        self.init_menu()
        self.forbidden_filename=""
        

    def forbidDeletion(self, filename):
        self.forbidden_filename = filename


    def showEvent(self, event):
        #print("show event")
        if not self.contacts_inited:
            asyncio.ensure_future(self.init_contacts())

    def closeEvent(self, event):
        #print("close!")
        import os, shutil
        folder = 'tempfiles/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) and os.path.basename(file_path) != os.path.basename(self.forbidden_filename):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    async def init_contacts(self):
        #print("init sections")
        if (self.fac_name is None) and (self.fac_id is None):
            return
        contacts = await self.api.get_faculty_info(self.fac_id, self.fac_name)
        urls = []
        for contact in contacts:
            urls.append(contact.img_url)

        contact_widgets = []
        loop = asyncio.get_event_loop()
        gather = GatherImages(loop)
        async with aiohttp.ClientSession() as session:
            img_paths = await gather.get_images(session, urls)
        for i in range(0, len(contacts)):
            cont_info = contacts[i]
            if img_paths[i]:
                contact_widget = Contact(cont_info.cont_id, cont_info.name, cont_info.position, cont_info.img_url, img_paths[i]
                    , cont_info.phone_number, cont_info.links, contacts_window=self)
            else:
                contact_widget = Contact(cont_info.cont_id, cont_info.name, cont_info.position, cont_info.img_url, 
                                contact_number=cont_info.phone_number, contact_links=cont_info.links, contacts_window=self)
            contact_widgets.append(contact_widget)

        self.preloader.stop_loader_animation()
        self.layout.removeWidget(self.preloader)
        self.preloader.hide()

        for contact_widget in contact_widgets:
            #section.clicked.connect(lambda: section.edit_clicked(self))
            self.layout.addWidget(contact_widget)

        self.layout.addStretch()
        self.contacts_inited = True


    def init_ui(self):
        widget = QWidget()
        self.layout = QVBoxLayout()
        #self.layout.setAlignment(Qt.AlignTop)
        widget.setLayout(self.layout)


        if self.fac_name or self.fac_id:
            #print("preloader!")
            self.preloader = Preloader()
            self.layout.addWidget(self.preloader)
        #self.layout.addWidget(Contact(1,"Горшков Сергей Андреевич", "разработчик"))
        #self.layout.addWidget(Contact(1,"Горшков Сергей Андреевич", "разработчик"))
        #self.layout.addWidget(Contact(1,"Горшков Сергей Андреевич", "разработчик"))

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
        self.head_label.setText("Контакты")
        #self.head_label.setMinimumHeight(50)
        #self.head_label.setMinimumWidth(100)
        #self.head_label.setMaximumWidth(300)
        #self.head_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.add_section_button = QPushButton("+")
        self.add_section_button.setFont(font)
        self.add_section_button.setMaximumWidth(100)
        self.add_section_button.clicked.connect(self.add_contact_clicked)

        head_layout.addWidget(self.head_label)
        head_layout.addWidget(self.add_section_button)


        navigation_font = QFont()
        navigation_font.setPointSize(12)

        navigation_layout = QHBoxLayout()
        self.button_back = QPushButton()
        self.button_back.setText("<")
        self.button_back.setMaximumWidth(30)
        self.button_back.setFont(navigation_font)
        self.button_back.clicked.connect(self.back_to_faculty_edit)

        navigation_label = QLabel()
        navigation_label.setText("Структурные подразделения/Редактирование СП/Контакты")
        navigation_label.setFont(navigation_font)

        navigation_layout.addWidget(self.button_back)
        navigation_layout.addWidget(navigation_label)
        navigation_layout.setAlignment(Qt.AlignTop)



        main_layout = QVBoxLayout()
        main_layout.addLayout(navigation_layout)
        main_layout.addLayout(head_layout)
        #main_layout.addWidget(self.head_label)
        #main_layout.addWidget(self.head_widget)
        main_layout.addWidget(self.scroller)
        main_layout.setAlignment(Qt.AlignTop)
        
        #main_layout.addStretch()
        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)



    def add_faculty_clicked(self):
        #print("clicked!")
        self.faculty_edit_window = faculty_edit.FacultyEditWindow(authorization_api=self.authorization_api)
        self.faculty_edit_window.move(self.pos())
        self.faculty_edit_window.resize(self.size())
        self.faculty_edit_window.show()
        self.close()
        #self.destroy()


    def back_to_faculty_edit(self):
        self.button_back.setEnabled(False)
        self.switch_to_edit_faculty(faculty_info=self.faculty_info)


    def switch_to_edit_faculty(self, faculty_info=None):
        self.section_edit_window = faculty_edit.FacultyEditWindow(faculty_info=faculty_info, authorization_api=self.authorization_api)
        self.section_edit_window.move(self.pos())
        self.section_edit_window.resize(self.size())
        self.section_edit_window.show()
        self.close()


    def switch_to_sbornic(self):
        self.sbornic_screen = section_screen.SectionsWindow(authorization_api=self.authorization_api)
        self.sbornic_screen.move(self.pos())
        self.sbornic_screen.resize(self.size())
        self.sbornic_screen.show()
        self.close()


    def switch_to_admins(self):
        self.admins_screen = admin_panel.AdminWindow(authorization_api=self.authorization_api, previousWindow=self)
        self.admins_screen.move(self.pos())
        self.admins_screen.resize(self.size())
        self.admins_screen.show()
        self.close()


    def faculties_list_action_triggered(self):
        self.faculties_window = faculties_screen.FacultiesWindow(authorization_api=self.authorization_api)
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()
    

    def add_contact_clicked(self):
        self.contact_window = contact_edit.ContactEditorWindow(faculty_info=self.faculty_info, authorization_api=self.authorization_api)
        self.contact_window.move(self.pos())
        self.contact_window.resize(self.size())
        self.contact_window.show()
        self.close()


    def open_contact_edit(self, contact_id, contact_name, contact_position, contact_number, photo_path, photo_url, contact_links):
        #print(photo_path)
        self.contact_window = contact_edit.ContactEditorWindow(self.faculty_info,
                contact_id, contact_name, contact_position, contact_number, 
                photo_path, photo_url, contact_links,
                authorization_api=self.authorization_api)
        self.contact_window.move(self.pos())
        self.contact_window.resize(self.size())
        self.contact_window.show()
        self.close()


    def init_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
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

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ScrollArea", "ИСП admin"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))
        self.admins_action.setText(_translate("MainWindow", "Админ-панель"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)


    contactsWindow = ContactsWindow()
    contactsWindow.show()

    with loop:
        #print("loop")
        loop.run_forever()
    #sys.exit(app.exec_())