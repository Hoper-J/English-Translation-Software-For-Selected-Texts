# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os

from PyQt5 import QtCore, QtGui, QtWidgets


class MenuBar(object):
    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.files = self.main_window.history_file.files
        self.symbols = {'self': self, 'QtWidgets': QtWidgets}
        self.set_menubar()
    def set_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")

        for i in range(1,4):
            exec(f"self.menu_{i} = QtWidgets.QMenu(self.menubar)", self.symbols)
            exec(f"self.menu_{i}.setObjectName('menu_{i}')", self.symbols)
        # self.menu_1 = QtWidgets.QMenu(self.menubar)
        # self.menu_1.setObjectName("menu_1")
        # self.menu_2 = QtWidgets.QMenu(self.menubar)
        # self.menu_2.setObjectName("menu_2")
        # self.menu_3 = QtWidgets.QMenu(self.menu_2)
        # self.menu_3.setObjectName("menu_3")
        self.main_window.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.actionimport_PDF = QtWidgets.QAction(self.main_window)
        self.actionimport_PDF.setObjectName("actionimport_PDF")
        self.actionlook_history_file = QtWidgets.QAction(self.main_window)
        self.actionlook_history_file.setObjectName("look_history_file")
        self.menu_1.addAction(self.actionimport_PDF)
        self.menu_1.addAction(self.actionlook_history_file)
        self.menu_2.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_1.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.change_pdf = self.main_window.signals.change_pdf
        # self.generate_latest_action = MainWindow.signals.generate_latest_action

        self.actionimport_PDF.triggered.connect(self._import_pdf)


        self._set_sizebar()
        self.retranslateUi(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def _set_function_bar(self):
        function_name = ['actionimport_PDF', 'look_history_file']

    def _set_sizebar(self):
        # 更简洁的方法来设置menubar
        # https://stackoverflow.com/questions/47044129/nameerror-name-self-is-not-defined-after-using-eval
        for i in range(8, 15):
            exec(f"self.action{i} = QtWidgets.QAction(self.main_window)", self.symbols)
            eval(f"self.action{i}.setObjectName('action{i}')")
            eval(f"self.action{i}.triggered.connect(lambda:self._change_font_size({i}))", self.symbols)
            eval(f"self.menu_3.addAction(self.action{i})")

    def _import_pdf(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self.main_window, "选取文件", os.getcwd(),
                                                                   "All Files(*);;Text Files(*.txt)")
        if fileName:
            """判断是否点击了cancel，如果cancel则不切换pdf"""
            print(fileType)
            self.change_pdf.emit(fileName)
            # self.generate_latest_action.emit(fileName)

    def generate_history_actions(self):
        """根据 history_file 生成对应的按钮"""
        total = len(self.files)
        for i in range(total):

            pass

    def _change_font_size(self, size):
        self.main_window.translate_text.setStyleSheet(f"font: {size}pt")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menu_1.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "更改字号"))
        self.actionimport_PDF.setText(_translate("MainWindow", "导入 PDF"))
        self.actionlook_history_file.setText(_translate("MainWindow", "历史文件"))
        self.action8.setText(_translate("MainWindow", "8"))
        self.action9.setText(_translate("MainWindow", "9"))
        self.action10.setText(_translate("MainWindow", "10"))
        self.action11.setText(_translate("MainWindow", "11"))
        self.action12.setText(_translate("MainWindow", "12"))
        self.action13.setText(_translate("MainWindow", "13"))
        self.action14.setText(_translate("MainWindow", "14"))


        # self.action8.setShortcut(_translate("MainWindow", "Meta+C"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MenuBar()
    ui.set_menubar(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
