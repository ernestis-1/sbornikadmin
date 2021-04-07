#работа с библиотекой PyQt5.QtGui(виджеты и прочее)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PIL import Image, ImageDraw

import os #работа с операционной системой
import sys#модуль sys(список аргументов командной строки)


class MainWindow(QMainWindow):# класс MainWindow

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
       #виджет отображает область редактирования
        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()  # QPlainTextEdit 
        #добавляем виджет в наше окно, просто создаем его как обычно, а затем устанавливаем в центральную позицию виджета для окна


        # настраиваем редактор для использования системного шрифта фиксированной ширины QFontDatabase.FixedFontс размером точек 12
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

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
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")
        
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
        
        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")#открыть файл
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")#сохранить текущую страницу
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
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
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")#отменить последнее изменение
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
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

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")#копировать выбранный текст
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")#вставить
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")#перенос текста в окно
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        self.show()

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
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

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

#результат
if __name__ == '__main__':
#конец пргораммы
    app = QApplication(sys.argv)
    app.setApplicationName("Текстовый редактор v 0.3")

    window = MainWindow()
    app.exec_()



