# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'card.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 188)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 131, 131))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(200, 60, 221, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(210, 90, 131, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(200, 110, 131, 21))
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(210, 40, 121, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">&lt;Здесь будет имя контакта&gt;</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">Должность:</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt;\">&lt;Должность&gt;</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:11pt;\">Имя контакта:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
