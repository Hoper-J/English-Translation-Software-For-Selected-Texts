import os


from PyQt5 import QtCore, QtWidgets


class MenuBar():
    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.files = self.main_window.history_file.files
        self.symbols = {'self': self, 'QtWidgets': QtWidgets,
                        "_translate": QtCore.QCoreApplication.translate}
        # todo: refactor
        self.set_menubar()
        self.last_total = len(self.files)
        # self.thread_menubar = threading.Thread(target=self.set_menubar) # 生成更新menu_bar的线程
        # self.thread_menubar.start()

    def set_menubar(self):
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")

        for i in range(1, 5):
            """
            (tree)
            menubar
            |__ 1：文件
            | |__ 导入pdf
            | |__ 3：历史文件
            |__ 2：编辑
            | |__ 4：字号
            """
            exec(
                f"self.menu_{i} = QtWidgets.QMenu(self.menubar)",
                self.symbols)
            exec(f"self.menu_{i}.setObjectName('menu_{i}')", self.symbols)

        self.menubar.addAction(self.menu_1.menuAction())  # 给menubar增加选项
        self.menubar.addAction(self.menu_2.menuAction())

        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        self.actionimport_PDF = QtWidgets.QAction(self.main_window)
        self.actionimport_PDF.setObjectName("actionimport_PDF")

        self._generate_history_actions()
        self._set_sizebar()  # 设置字号的action和triggered

        self.menu_1.addAction(self.actionimport_PDF)
        self.menu_1.addAction(self.menu_3.menuAction())
        self.menu_2.addAction(self.menu_4.menuAction())

        self.change_pdf = self.main_window.signals.change_pdf

        self.actionimport_PDF.triggered.connect(self._import_pdf)

        self.retranslateUi(self.main_window)  # 重命名action的显示名字

        self.main_window.setMenuBar(self.menubar)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def _generate_history_actions(self):
        """根据 history_file 生成对应的按钮"""
        total = len(self.files)
        for i in range(total):
            # 注意，历史记录应为倒序排列
            filename = os.path.basename(self.files[i])
            exec(
                f"self.file{i} = QtWidgets.QAction(self.main_window)",
                self.symbols)
            eval(f"self.file{i}.setObjectName('file{i}')")
            eval(
                f"self.file{i}.triggered.connect(lambda:self._change_pdf('{self.files[i]}'))",
                self.symbols)
            eval(
                f"self.file{i}.setText(_translate('MainWindow', '{filename}'))",
                self.symbols)
            eval(f"self.menu_3.addAction(self.file{i})")
            pass

    def _update_history_actions(self, pdf=None):
        """在切换pdf时更新历史记录"""
        total = len(self.files)
        if total > self.last_total:
            # 通过对比当前历史记录和之前历史记录的数量，来判断是否导入了新的pdf
            if total < 10:
                # 如果大于上一次历史记录的数量且小于10，那么代表导入了新的pdf，需要创建新action
                exec(
                    f"self.file{total-1} = QtWidgets.QAction(self.main_window)",
                    self.symbols)
                eval(f"self.menu_3.addAction(self.file{total-1})")
                self.last_total = total  # 更新当前历史记录数量
            for i in range(total):
                filename = os.path.basename(self.files[i])
                eval(f"self.file{i}.setObjectName('file{i}')")
                eval(
                    f"self.file{i}.triggered.connect(lambda:self._change_pdf('{self.files[i]}'))",
                    self.symbols)
                eval(
                    f"self.file{i}.setText(_translate('MainWindow', '{filename}'))",
                    self.symbols)

        # else:
        #     if total < 10:
        #         exec(f"self.file{total-1} = QtWidgets.QAction(self.main_window)", self.symbols)
        #         eval(f"self.menu_3.addAction(self.file{total-1})")
        #         self.last_total = total # 更新当前历史记录数量
        #     for i in range(total):
        #         filename = os.path.basename(self.files[i])
        #         eval(f"self.file{i}.setObjectName('file{i}')")
        #         eval(f"self.file{i}.triggered.connect(lambda:self._change_pdf('{self.files[i]}'))", self.symbols)
        #         eval(f"self.file{i}.setText(_translate('MainWindow', '{filename}'))", self.symbols)

    def _set_sizebar(self):
        # 设置字号栏
        # https://stackoverflow.com/questions/47044129/nameerror-name-self-is-not-defined-after-using-eval
        for i in range(8, 15):
            exec(
                f"self.size{i} = QtWidgets.QAction(self.main_window)",
                self.symbols)
            eval(f"self.size{i}.setObjectName('size{i}')")
            eval(
                f"self.size{i}.triggered.connect(lambda:self._change_pdf({i}))",
                self.symbols)
            eval(
                f"self.size{i}.setText(_translate('MainWindow', '{i}'))",
                self.symbols)
            eval(f"self.menu_4.addAction(self.size{i})")

    def _import_pdf(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if fileName:
            """判断是否点击了cancel，如果cancel则不切换pdf"""
            # print(fileType)
            self.change_pdf.emit(fileName)
            self._update_history_actions(fileName)  # 导入新pdf更新历史记录
            # self.generate_latest_action.emit(fileName)

    def _change_pdf(self, pdf):
        self.change_pdf.emit(pdf)

        self._update_history_actions(pdf)  # 切换pdf更新历史记录

    def _change_font_size(self, size):
        self.main_window.translate_text.setStyleSheet(f"font: {size}pt")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.menu_1.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "历史记录"))
        self.menu_4.setTitle(_translate("MainWindow", "更改字号"))
        self.actionimport_PDF.setText(_translate("MainWindow", "导入 PDF"))

        # self.action8.setShortcut(_translate("MainWindow", "Meta+C"))
