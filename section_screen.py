import asyncio
import aiohttp

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from quamash import QEventLoop
from sections_api import SectionInfo, SectionsApi
from images_api import GatherImages
from global_constants import SECTIONS_API
from preloader import Preloader
#from section_edit import SectionEditWindow
import section_edit, redakt4
import faculties_screen, admin_panel
from authorization_api import AuthorizationApi

class Section(QPushButton):
    def __init__(self, sect_id=-1, img_path=None, section_name="section name", sectionsWindow=None):
        QPushButton.__init__(self, parent=None)
        self.sect_id = sect_id
        self.img_path = img_path
        self.section_name = section_name
        self.sectionsWindow = sectionsWindow
        self.__init_ui__(img_path)
        self.clicked.connect(self.edit_clicked)

    def __init_ui__(self, img_path):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setMaximumHeight(150)
        self.setMinimumHeight(140)

        label = QtWidgets.QLabel(self)
        #self.label.setGeometry(QtCore.QRect(40, 50, 151, 141))
        label.setMaximumHeight(120)
        label.setMaximumWidth(120)
        label.setText("")
        label.setPixmap(QtGui.QPixmap(img_path))
        label.setScaledContents(True)
        label.setObjectName("label")
        layout.addWidget(label)
        #layout.addStretch(0)
        #layout.setAlignment(Qt.AlignLeft)

        label_2 = QtWidgets.QLabel(self)
        #self.label_2.setGeometry(QtCore.QRect(220, 60, 241, 101))
        label_2.setMinimumHeight(120)
        font = QFont()
        font.setPointSize(14)
        label_2.setFont(font)
        label_2.setText(self.section_name)
        label_2.setAutoFillBackground(False)
        label_2.setWordWrap(True)
        label_2.setTextFormat(QtCore.Qt.AutoText)
        label_2.setScaledContents(False)
        label_2.setObjectName("label_2")
        label_2.setMargin(10)
        layout.addWidget(label_2)

    def get_id(self):
        return self.sect_id

    def edit_clicked(self):
        self.sectionsWindow.forbidDeletion(self.img_path)
        self.setEnabled(False)
        #print("edit clicked")
        self.sectionsWindow.switch_to_edit_section(self.sect_id, self.section_name, self.img_path)


class SectionsWindow(QMainWindow, QWidget):
    #async_sections_sygnal = pyqtSignal()

    def __init__(self, authorization_api=AuthorizationApi()):
        super(SectionsWindow, self).__init__()
        self.resize(800, 600)
        self.authorization_api = authorization_api
        self.api = SectionsApi(SECTIONS_API)
        self.sections_inited = False
        self.init_ui()
        self.init_menu()
        self.forbidden_filename=""
        #self.async_sections_sygnal.connect(self.wrap)
        #self.async_sections_sygnal.emit()
        #self.init_sections()
        
    def forbidDeletion(self, filename):
        self.forbidden_filename = filename

    def showEvent(self, event):
        #print("show event")
        if not self.sections_inited:
            asyncio.ensure_future(self.init_sections())

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


    async def init_sections(self):
        #print("init sections")
        self.sections = await self.api.get_sections()

        urls = []
        for sect in self.sections:
            urls.append(sect.img_url)

        sections = []
        loop = asyncio.get_event_loop()
        gather = GatherImages(loop)
        images = await gather.get_many_images(urls)
        for i in range(0, len(self.sections)):
            image_path = images[i]
            section_info = self.sections[i]
            if (image_path):
                section = Section(section_name=section_info.name, sect_id=section_info.sect_id, img_path=image_path, sectionsWindow=self)
                sections.append(section)
                    #self.layout.addWidget(section)
            else:
                section = Section(section_name=section_info.name, sect_id=section_info.sect_id, sectionsWindow=self)
                #section.clicked.connect(lambda: section.edit_clicked(self))
                sections.append(section)
                #self.layout.addWidget(section)
        
        self.preloader.stop_loader_animation()
        self.layout.removeWidget(self.preloader)
        self.preloader.hide()

        for section in sections:
            #section.clicked.connect(lambda: section.edit_clicked(self))
            self.layout.addWidget(section)

        self.layout.addStretch()
        self.sections_inited = True


    def add_section_clicked(self):
        #print("clicked!")
        self.add_section_button.setEnabled(False)
        self.section_edit_window = section_edit.SectionEditWindow(authorization_api=self.authorization_api)
        self.section_edit_window.move(self.pos())
        self.section_edit_window.resize(self.size())
        if self.isMaximized():
            self.section_edit_window.showMaximized()
        else:
            self.section_edit_window.show()
        self.close()
        #self.destroy()


    def switch_to_faculty(self):
        self.faculties_window = faculties_screen.FacultiesWindow(authorization_api=self.authorization_api)
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        if self.isMaximized():
            self.faculties_window.showMaximized()
        else:
            self.faculties_window.show()
        self.close()

    
    def switch_to_admins(self):
        self.admins_screen = admin_panel.AdminWindow(authorization_api=self.authorization_api, previousWindow=self)
        self.admins_screen.move(self.pos())
        self.admins_screen.resize(self.size())
        if self.isMaximized():
            self.admins_screen.showMaximized()
        else:
            self.admins_screen.show()
        self.close()


    def switch_to_edit_section(self, sect_id, sect_name, sect_img):
        self.section_edit_window = section_edit.SectionEditWindow(sect_id=sect_id, name=sect_name, filepath=sect_img, authorization_api=self.authorization_api,
            last_screen=self)
        self.section_edit_window.move(self.pos())
        self.section_edit_window.resize(self.size())
        if self.isMaximized():
            self.section_edit_window.showMaximized()
        else:
            self.section_edit_window.show()
        self.close()


    def redakt_action_triggered(self):
        self.redakt_window = redakt4.EditorWindow(authorization_api=self.authorization_api)
        self.redakt_window.move(self.pos())
        self.redakt_window.resize(self.size())
        if self.isMaximized():
            self.redakt_window.showMaximized()
        else:
            self.redakt_window.show()
        self.close()

    def init_ui(self):
        widget = QWidget()
        self.layout = QVBoxLayout()
        #self.layout.setAlignment(Qt.AlignTop)
        widget.setLayout(self.layout)

        
        self.preloader = Preloader()
        self.layout.addWidget(self.preloader)
        

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
        self.head_label.setText("Разделы сборника")
        #self.head_label.setMinimumHeight(50)
        #self.head_label.setMinimumWidth(100)
        #self.head_label.setMaximumWidth(300)
        #self.head_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.add_section_button = QPushButton("+")
        self.add_section_button.setFont(font)
        self.add_section_button.setMaximumWidth(100)
        self.add_section_button.clicked.connect(self.add_section_clicked)

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
        
        self.faculty_action = QtWidgets.QAction(self)
        self.faculty_action.setObjectName("action_5")
        self.faculty_action.triggered.connect(self.switch_to_faculty)
        
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
        self.setWindowTitle(_translate("MainWindow", "ИСП admin"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))
        self.admins_action.setText(_translate("MainWindow", "Админ-панель"))


        
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    authorization_api = AuthorizationApi()
    MainWindow = SectionsWindow(authorization_api=authorization_api)
    MainWindow.showMaximized()
    #print("show")
    
    with loop:
        #print("loop")
        loop.run_forever()

    #sys.exit(app.exec_())

if __name__ == "__main__":
    main()
