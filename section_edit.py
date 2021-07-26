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
from sections_api import SectionsApi, ArticleInfo
from preloader import Preloader
import section_screen
import redakt4
import faculties_screen
import global_constants
import requests
import asyncio

class Article(QPushButton):
    def __init__(self, article_info=None, sectionEditWindow=None):
        QPushButton.__init__(self, text=article_info.article_title)
        self.article_id = article_info.article_id
        self.article_title = article_info.article_title
        self.sectionEditWindow = sectionEditWindow
        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.clicked.connect(self.edit_article_clicked)
        #self.setFixedWidth(450)

    def edit_article_clicked(self):
        print(self.article_id)
        if (self.sectionEditWindow):
            self.setEnabled(False)
            self.sectionEditWindow.edit_article_triggered(self.article_id, self.article_title)



class SectionEditWindow(QMainWindow):
    def __init__(self, sect_id=None, name=None, filepath=None, img_url=None):
        super().__init__()
        
        #existing section parameters
        self.sect_id = sect_id
        self.name = name
        self.image_file_name = filepath
        self.img_url = img_url
        self.loading = (sect_id is not None)
        
        self.api = SectionsApi(global_constants.SECTIONS_API)
        
        self.is_keep_path = False
        self.resize(800, 600)
        self.init_ui()
        self.init_menu()
        self.status = QStatusBar()
        self.setStatusBar(self.status)


    def init_ui(self):
        self.title_layout = QVBoxLayout()

        self.line_input_head = QLineEdit(self)#QPlainTextEdit
        #font_head = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font_input = QFont()
        font_input.setPointSize(14)
        self.line_input_head.setFont(font_input)
        if (self.name):
            self.line_input_head.setText(self.name)
        self.line_input_head.setCursorPosition(0)

        font_head = QFont()
        font_head.setPointSize(12)

        self.label_head = QLabel("Название раздела:")
        self.label_head.setFont(font_head)

        self.button_create = QPushButton('Создать раздел')
        if (self.sect_id):
            self.button_create.setText('Отправить изменения')
        
        self.button_create.setFont(font_head)
        self.button_create.setMinimumHeight(45)
        self.button_create.clicked.connect(self.edit_section_clicked)

        self.title_layout.addWidget(self.label_head)
        self.title_layout.addWidget(self.line_input_head)
        #title_layout.addStretch()
        self.title_layout.addWidget(self.button_create)
        #self.title_layout.addStretch()
        self.title_layout.setAlignment(Qt.AlignTop)


        self.attachment_layout = QVBoxLayout()

        self.label_image = QLabel()
        self.label_image.setScaledContents(True)
        label_size = 175
        self.label_image.setMaximumWidth(label_size)
        self.label_image.setMaximumHeight(label_size)
        self.label_image.setMinimumWidth(label_size)
        self.label_image.setMinimumHeight(label_size)
        
        if (self.image_file_name):
            pixmap = QPixmap(self.image_file_name)
        else:
            pixmap = QPixmap("images/attach.png")
        self.label_image.setPixmap(pixmap)

        self.button_font = QFont()
        self.button_font.setPointSize(10)

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.setFont(self.button_font)
        self.button_open.clicked.connect(self._on_open_image)
        self.button_open.setMaximumWidth(200)

        

        self.attachment_layout.addWidget(self.label_image)
        self.attachment_layout.addWidget(self.button_open)
        #self.attachment_layout.addWidget(self.button_delete)
        #self.attachment_layout.addStretch()
        self.attachment_layout.setAlignment(Qt.AlignTop)
        #attachment_layout.addWidget(self.button_delete)
        if (self.sect_id):
            self.add_delete_button()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(self.attachment_layout)
        horizontal_layout.addLayout(self.title_layout)

        #self.controlWidget = QWidget()
        #self.controlWidget.setLayout(horizontal_layout)
        #self.controlWidget.setMinimumHeight(100)


        main_layout = QVBoxLayout()

        
        #self.button_create.clicked.connect(self._on_save_as_image)
        navigation_font = QFont()
        navigation_font.setPointSize(12)

        navigation_layout = QHBoxLayout()
        self.button_back = QPushButton()
        self.button_back.setText("<")
        self.button_back.setMaximumWidth(30)
        self.button_back.setFont(navigation_font)
        self.button_back.clicked.connect(self.sections_list_action_triggered)

        navigation_label = QLabel()
        navigation_label.setText("Сборник/Редактирование раздела")
        navigation_label.setFont(navigation_font)

        navigation_layout.addWidget(self.button_back)
        navigation_layout.addWidget(navigation_label)
        navigation_layout.setAlignment(Qt.AlignTop)

        main_layout.addLayout(navigation_layout)
        main_layout.addLayout(horizontal_layout)
        main_layout.setAlignment(Qt.AlignTop)
        #main_layout.addWidget(self.controlWidget)
        #main_layout.addWidget(self.button_create)
        #main_layout.addStretch()
        #self.setLayout(main_layout)

        if self.sect_id:
            self.init_article_area()

        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)


    def showEvent(self, event):
        if self.sect_id and self.loading:
            self.loading = True
            asyncio.ensure_future(self.init_articles())


    def init_article_area(self):
        self.scrollerLayout = QVBoxLayout()
        scrollerWidget = QWidget()
        scrollerWidget.setLayout(self.scrollerLayout)

        self.scroller = QScrollArea()
        #self.setCentralWidget(self.scroller)
        #self.scroller.setFixedWidth(650)
        #self.scroller.setMinimumHeight(350)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)

        self.scroller.setWidget(scrollerWidget)

        head_article_list_layout = QHBoxLayout()
        
        self.article_list_head_widget = QWidget()
        #self.article_list_head_widget.setFixedWidth(662)
        #self.article_list_head_widget.setLayout(head_article_list_layout)

        font = QtGui.QFont()
        font.setPointSize(12)

        self.head_article_list_label = QLabel()
        self.head_article_list_label.setFont(font)
        self.head_article_list_label.setText("Статьи")
        #self.head_label.setMinimumHeight(50)
        #self.head_label.setMinimumWidth(100)
        #self.head_label.setMaximumWidth(300)
        #self.head_article_list_label.setAlignment(Qt.AlignCenter)

        self.add_article_button = QPushButton("+")
        self.add_article_button.setFont(font)
        self.add_article_button.setMaximumWidth(100)
        self.add_article_button.clicked.connect(lambda: self.edit_article_triggered(article_id=None, article_name=None))

        head_article_list_layout.addWidget(self.head_article_list_label)
        head_article_list_layout.addWidget(self.add_article_button)

        self.article_area_layout = QVBoxLayout()
        #self.article_area_layout.addWidget(self.article_list_head_widget)
        self.article_area_layout.addLayout(head_article_list_layout)
        self.article_area_layout.addWidget(self.scroller)

        self.main_scroll_widget = QGroupBox()
        self.main_scroll_widget.setLayout(self.article_area_layout)

        self.title_layout.insertWidget(self.title_layout.count()-1, self.main_scroll_widget)
        #self.title_layout.addWidget(self.main_scroll_widget)
        #self.title_layout.insertStretch(self.title_layout.count()-1,10)
        #self.title_layout.insertLayout(self.title_layout.count()-1, self.article_area_layout)

        if self.loading:
            #print("preloader")
            self.preloader = Preloader()
            self.scrollerLayout.addWidget(self.preloader)    
        else:
            self.preloder = None
            #print("no preloader")


    async def init_articles(self):
        #print("init articles")
        article_infos = await self.api.get_articles(self.sect_id)
        self.preloader.stop_loader_animation()
        self.scrollerLayout.removeWidget(self.preloader)
        self.preloader.hide()
        self.loading = False
        if article_infos is None:
            return
        #self.article_buttons = []
        for article_info in article_infos:
            article = Article(article_info, self)
            self.scrollerLayout.addWidget(article)
            #self.article_buttons.append()
        self.scrollerLayout.addStretch()


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
        self.faculty_action.triggered.connect(self.switch_to_faculty)
        
        self.menu_screens.addAction(self.sections_list_action)
        #self.menu_screens.addAction(self.section_creation)
        self.menu_screens.addAction(self.article_creation)
        
        self.menu_modes.addAction(self.sbornic_action)
        self.menu_modes.addAction(self.faculty_action)
        
        self.menubar.addAction(self.menu_modes.menuAction())
        #self.menubar.addAction(self.menu_screens.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "ИСП admin"))
        self.menu_screens.setTitle(_translate("MainWindow", "Экраны"))
        self.menu_modes.setTitle(_translate("MainWindow", "Режим"))
        self.sections_list_action.setText(_translate("MainWindow", "Список разделов"))
        #self.section_creation.setText(_translate("MainWindow", "Создание раздела"))
        self.article_creation.setText(_translate("MainWindow", "Создание статьи"))
        self.sbornic_action.setText(_translate("MainWindow", "Сборник"))
        self.faculty_action.setText(_translate("MainWindow", "Факультет"))


    def add_delete_button(self):
        self.button_delete = QPushButton("Удалить раздел")
        #self.button_delete.setText("Удалить")
        self.button_delete.setFont(self.button_font)
        self.button_delete.setIcon(QIcon("images/bin.png"))
        self.button_delete.setIconSize(QSize(20,20))
        #self.button_delete.setMaximumWidth(50)
        self.button_delete.clicked.connect(self.delete_section)
        
        #self.attachment_layout.insertWidget(self.attachment_layout.count()-1, self.button_delete)
        self.attachment_layout.addWidget(self.button_delete)
        #self.attachment_layout.addStretch()


    def delete_section(self):
        if self.sect_id is None:
            return
        #payload = {'id': self.sect_id}
        try:
            r = requests.delete(global_constants.ARTICLE_API+f"/{self.sect_id}")
            if (r.status_code == 200):
                self.status.showMessage("Раздел удалён!")
                self.sections_list_action_triggered()
            else:
                self.status.showMessage("Ошибка при удалении. Возможно, этот раздел нельзя удалить")
                print(r.status_code)
        except Exception as e:
            self.status.showMessage("Ошибка при отправке запроса!")


    def closeEvent(self, event):
        if self.is_keep_path:
            return
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


    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return
        self.image_file_name = file_name
        self.img_url = None
        pixmap = QPixmap(file_name)
        self.label_image.setPixmap(pixmap)

    def sections_list_action_triggered(self):
        self.button_back.setEnabled(False)
        self.sections_window = section_screen.SectionsWindow()
        self.sections_window.move(self.pos())
        self.sections_window.resize(self.size())
        self.sections_window.show()
        self.close()
        #self.destroy()

    def edit_article_triggered(self, article_id=None, article_name=None):
        #print("triggered!")
        if (self.loading):
            return
        #print(article_id is None)
        self.add_article_button.setEnabled(False)
        self.is_keep_path = True
        self.article_window = redakt4.EditorWindow(article_id=article_id, parent_id=self.sect_id, article_name=article_name,
                                sect_name=self.name, sect_img_path=self.image_file_name, sect_img_url=self.img_url)
        self.article_window.move(self.pos())
        self.article_window.resize(self.size())
        self.article_window.show()
        self.close()


    def redakt_action_triggered(self):
        self.redakt_window = redakt4.EditorWindow()
        self.redakt_window.move(self.pos())
        self.redakt_window.resize(self.size())
        self.redakt_window.show()
        self.close()

    def switch_to_faculty(self):
        self.faculties_window = faculties_screen.FacultiesWindow()
        self.faculties_window.move(self.pos())
        self.faculties_window.resize(self.size())
        self.faculties_window.show()
        self.close()


    def edit_section_clicked(self):
        #print("edit section")
        s = self.button_create.text()
        if self.sect_id is None:
            print("here")
            self.button_create.setText("Отправить изменения")
            try:
                #print(self.line_input_head.text())
                j = {
                        "isMain": True,
                        "title": str(self.line_input_head.text()),
                        "picture": "",
                        "parentId": -1
                    }
                if (self.image_file_name):
                    j["picture"] = redakt4.get_photo_uri(self.image_file_name)
                #print(j)
                r = requests.post(global_constants.ARTICLE_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Раздел создан!")
                    #print(r.json())
                    self.sect_id = r.json()['id']
                    self.name = r.json()['title']
                    self.add_delete_button()
                    #self.just_created = True
                    self.init_article_area()
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка!")
                print(e)
            #self.status.showMessage("Раздел создан!")
        else:
            j = {
                    "id": self.sect_id,
                    "isMain": True,
                    "title": str(self.line_input_head.text()),
                    "picture": "",
                    "parentId": -1
                }
            if self.img_url:
                j["picture"] = self.img_url
            else:
                if (self.image_file_name):
                    try:
                        j["picture"] = redakt4.get_photo_uri(self.image_file_name)
                    except Exception as e:
                        print(e)
                else:
                    pass
            try:
                r = requests.put(global_constants.ARTICLE_API, json=j)
                if (r.status_code == 200):
                    self.status.showMessage("Изменения отправлены!")
                    #print(r.json())
                    self.sect_id = r.json()['id']
                    self.name = r.json()['title']
                else:
                    print(r.status_code)
            except Exception as e:
                self.status.showMessage("Ошибка при отправке!")
            #print("section exists")

            


if __name__ == '__main__':
    app = QApplication([])

    mw = SectionEditWindow()
    mw.show()

    app.exec()
