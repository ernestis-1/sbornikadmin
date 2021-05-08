# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from sections_api import SectionInfo, SectionsApi
from global_constants import SECTIONS_API
from preloader import Preloader
from quamash import QEventLoop
import asyncio


class Section(QPushButton):
    def __init__(self, sect_id=-1, img_path="../../Users/caisilus/Pictures/Saved Pictures/S8HLlscvIvk.jpg", section_name="section name"):
        QPushButton.__init__(self, parent=None)
        self.sect_id = sect_id
        self.__init_ui__(img_path, section_name)

    def __init_ui__(self, img_path, section_name):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setMaximumHeight(200)
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
        #layout.addStretch(1)

        label_2 = QtWidgets.QLabel(self)
        #self.label_2.setGeometry(QtCore.QRect(220, 60, 241, 101))
        label_2.setMinimumHeight(120)
        font = QtGui.QFont()
        font.setPointSize(14)
        label_2.setFont(font)
        label_2.setText(section_name)
        label_2.setAutoFillBackground(False)
        label_2.setTextFormat(QtCore.Qt.AutoText)
        label_2.setScaledContents(False)
        label_2.setObjectName("label_2")
        layout.addWidget(label_2)

    def get_id(self):
        return self.sect_id

class SectionsWindow(QMainWindow, QWidget):
    #async_sections_sygnal = pyqtSignal()

    def __init__(self):
        super(SectionsWindow, self).__init__()
        self.resize(800, 600)
        self.api = SectionsApi(SECTIONS_API)
        self.init_ui()
        #self.async_sections_sygnal.connect(self.wrap)
        #self.async_sections_sygnal.emit()
        #self.init_sections()
        
    def showEvent(self, event):
        print("show event")
        asyncio.ensure_future(self.init_sections())

    async def init_sections(self):
        print("init sections")
        self.sections = await self.api.get_sections()
        self.preloader.stop_loader_animation()
        self.layout.removeWidget(self.preloader)
        self.preloader.hide()
        for section_info in self.sections:
            if (section_info.img_url):
                section = Section(section_name=section_info.name, sect_id=section_info.sect_id, img_path=section_info.img_url)
                self.layout.addWidget(section)
            else:
                section = Section(section_name=section_info.name, sect_id=section_info.sect_id)
                self.layout.addWidget(section)


    def init_ui(self):
        widget = QWidget()
        self.layout = QVBoxLayout()
        widget.setLayout(self.layout)

        
        self.preloader = Preloader()
        self.layout.addWidget(self.preloader)
        

        self.scroller = QScrollArea()
        #self.setCentralWidget(self.scroller)
        self.scroller.setFixedWidth(700)
        self.scroller.setMinimumHeight(150)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        
        self.scroller.setWidget(widget)
        #self.scroller.adjustSize()

        font = QtGui.QFont()
        font.setPointSize(14)
        self.head_label = QLabel()
        self.head_label.setFont(font)
        self.head_label.setText("Разделы сборника")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.head_label)
        main_layout.addWidget(self.scroller)
        
        #main_layout.addStretch()
        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)

        
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    MainWindow = SectionsWindow()
    MainWindow.show()
    print("show")
    
    with loop:
        print("loop")
        loop.run_forever()

    #sys.exit(app.exec_())

if __name__ == "__main__":
    main()