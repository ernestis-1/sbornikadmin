#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtPrintSupport import *


import os #работа с операционной системой

import sys#модуль sys(список аргументов командной строки)

import requests

import uuid



FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64]
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp','.jpeg']
HTML_EXTENSIONS = ['.htm', '.html']


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        self.label_nazv = QLineEdit()#QPlainTextEdit
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)

       

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)

        self.button_save_as = QPushButton('Сохранить картинку')
        self.button_save_as.clicked.connect(self._on_save_as_image)

        

       

        self.label_image = QLabel()

        self.label_nazvprot = QLabel("Введите название для статьи:")

        # Путь сохранения файла
        self.save_file_name = 'C:\img.jpg'

        
        main_layout.addWidget(self.button_open)
        main_layout.addWidget(self.button_save_as)
        main_layout.addWidget(self.label_image)
        main_layout.addWidget(self.label_nazvprot)
        main_layout.addWidget(self.label_nazv)
       
        

        self.setLayout(main_layout)

    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        pixmap = QPixmap(file_name)
        self.label_image.setPixmap(pixmap)

    def _on_save_as_image(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", 'img.jpg', "Image (*.png *.jpg)")[0]
        if not file_name:
            return
        
        self.label_image.pixmap().save(file_name)



    def file_saveas(self):#функция для сохранения файла как
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt All files (*.*)")

        if not path:
            # Если было отменено, то вернется - ''
            return

        self._save_to_path(path)



def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    return os.path.splitext(p)[1].lower()

class TextEdit(QTextEdit):

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():

            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                   
                    break

            else:
                # If all were valid images, finish here.
                return


        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)






class MainWindow(QMainWindow, QWidget):# класс MainWindow

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
       #виджет отображает область редактирования
        layout = QVBoxLayout()

        self.label_nazvprot = QLabel("Введите название для статьи:")

        layout.addWidget(self.label_nazvprot)
        
        self.label_nazv = QLineEdit()
        fixedfontnazv = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        fixedfontnazv.setPointSize(18)
        self.label_nazv.setFont(fixedfontnazv)

        layout.addWidget(self.label_nazv)
        
        self.editor = TextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)

        font = QFont('Times', 12)
        self.editor.setFont(font)

        self.editor.setFontPointSize(12)

       
        

        # self.path(содержит путь к текущему открытому файлу)
        # Если "None", получается, что файл еще не открыт (или создается новый).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)


        file_toolbar = QToolBar("File")#файл
        file_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        self.razdel = QPushButton('Переход в создание раздела')
        self.razdel.clicked.connect(self.buttonClicked)

        self.button_open = QPushButton('Выбрать картинку')
        self.button_open.clicked.connect(self._on_open_image)

        self.button_save_as = QPushButton('Сохранить картинку')
        self.button_save_as.clicked.connect(self._on_save_as_image)

        


        self.label_image = QLabel("<Файл>")
        


       
        layout.addWidget(self.razdel)
        layout.addWidget(self.button_open)
        layout.addWidget(self.button_save_as)
        layout.addWidget(self.label_image)
        
        

        
        
       

        
        
        #.clear()	Очистить выделенный текст
        #.cut() 	Вырезать выделенный текст в буфер обмена
        #.copy()	Копировать выделенный текст в буфер обмена
        #.paste()	Вставить буфер обмена под курсором
        #.undo()	Отменить последнее действие
        #.redo()	Повторить последнее отмененное действие
        #.insertPlainText(text)     Вставить обычный текст под курсором
        #.selectAll()	 Выделить весь текст в документе
        
        # редактор  умеет выполнять множество стандартных операций - копировать, вырезать, вставлять, очищать
        # виджет обеспечивает поддержку всего этого через слоты Qt
        
        # набор кнопок панели инструментов для редактирования, каждая из которых определяется как QAction
        # Подключение .triggeredсигнала от QActionк соответствующему слоту включает определенное поведение
        
        open_file_action = QAction(QIcon(os.path.join('images', 'blueopen.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")#открыть файл
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")#сохранить текущую страницу
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk2.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")#сохранить текущую страницу в указанный файл
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")#напечатать текущую страницу
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")#редактировать
        edit_toolbar.setIconSize(QSize(18, 18))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'x.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")#отменить последнее изменение
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'redo.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")#повторить последнее изменение
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")#вырезать выбранный текст
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")#копировать выбранный текст
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'paste.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")#вставить
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'all.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'wind.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")#перенос текста в окно
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction(QIcon(os.path.join('images', 'italic-icon.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction(QIcon(os.path.join('images', 'under.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.alignl_action = QAction(QIcon(os.path.join('images', 'left.png')), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon(os.path.join('images', 'center.png')), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon(os.path.join('images', 'right.png')), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(QIcon(os.path.join('images', 'justt.png')), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        format_menu.addSeparator()

        # format
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # signal
        ]

       
        self.update_format()
        self.update_title()
        self.show()

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """   
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)


        

        #self.resize(650, 650)
        #self.update_format()
        #self.update_title()
        #self.show()


             

    def dialog_critical(self, s):#обработка MessageBox
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

        
   


   
        
#определяем file_open метод, который при запуске использует QFileDialog.getOpenFileName
#для отображения диалогового окна открытия файла платформы
#выбранный путь затем используется для открытия файла 
#
    def file_open(self):#функция для открытия файла
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
         #конструкции try except
        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

        

    
#два блока для сохранения файлов - save и save_as
#первый для сохранения открытого файла, у которого уже есть имя файла, второй для сохранения нового файла
    def file_save(self):#функция для сохранения файла
        if self.path is None:
            # Если нет пути, то нужно использовать сохранение как
            return self.file_saveas()

        self._save_to_path(self.path)#сохранение

    def file_saveas(self):#функция для сохранения файла как
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt All files (*.*)")

        if not path:
            # Если было отменено, то вернется - ''
            return

        self._save_to_path(path)
# в любом случае выполняется само сохранение, _save_to_path()которое принимает целевой путь   
    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:#конструкция try except
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

       
    #настройка печати
    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Текстовый редактор v 0.3" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

    def buttonClicked(self):
        #from newscreen
        #from newscreen import NewWindow
        
        self.exPopup = NewWindow()
        self.exPopup.setWindowTitle("Создание раздела")
        self.exPopup.setGeometry(100, 200, 100, 100)
        self.exPopup.show()
        
        
    def _on_open_image(self):
        file_name = QFileDialog.getOpenFileName(self, "Выбор картинки", None, "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        filepath = file_name.split("/")[-1]
        #file_name1 = file_name.resize((10, 10))
        
        pixmap = QPixmap(file_name)
        
        self.label_image.setText(filepath)
        
        #self.label_image.setPixmap(pixmap)
        
        
        
        
       
        

    def _on_save_as_image(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение картинки", 'img.jpg', "Image (*.png *.jpg)")[0]
        if not file_name:
            return

        self.label_image.pixmap().save(file_name)


def get_photo_uri(path_img):
    url = 'https://api.imgbb.com/1/upload?key=7739426e6cc4b2afe15d5db0e8272009'
    with open(path_img, 'rb') as img:
        name_img = os.path.basename(path_img)
        files = {'image': (name_img,img, 'multipart/form-data', {'Expires': '0'}) }
        with requests.Session() as s:
            r = s.post(url,files=files)
            #print(r.status_code)
            #print(r.text)
            json_response = r.json()
            url_data = json_response['data']
            print(f'Нужный url: {url_data["url"]}')
            return url_data["url"]


#результат
if __name__ == '__main__':
#конец программы
    app = QApplication(sys.argv)
    app.setApplicationName("Текстовый редактор v 0.3")
    window = MainWindow()
    app.exec_()
    





