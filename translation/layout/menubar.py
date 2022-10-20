import multiprocessing
import os
import shutil
import threading

from multiprocessing import Process

import PyPDF2
import ocrmypdf
from PyQt5 import QtCore, QtWidgets

from translation.const import CONST

class MenuBar():
    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.files = self.main_window.history_files.files
        self.symbols = {'self': self, 'QtWidgets': QtWidgets,
                        "_translate": QtCore.QCoreApplication.translate}
        # todo: refactor
        self.set_menubar()
        self.set_statusbar()

        m = multiprocessing.Manager()
        self.OCR_queue = m.Queue()

        self.detection_ocr_achieved = threading.Thread(
            target=self._detection_ocr_achieved, daemon=True)
        self.detection_ocr_achieved.start()

        self._process = QtCore.QProcess()
        self._process.started.connect(self._ocr)
        # self._process.finished.connect(self.handleFinished)
        self._timer = QtCore.QTimer()

        self.last_total = len(self.files)

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
            | |__ 清空历史查询
            | |__ OCR
            | |__ 4：字号
            """
            exec(
                f"self.menu_{i} = QtWidgets.QMenu(self.menubar)",
                self.symbols)
            exec(f"self.menu_{i}.setObjectName('menu_{i}')", self.symbols)

        self.menubar.addAction(self.menu_1.menuAction())  # 给menubar增加选项
        self.menubar.addAction(self.menu_2.menuAction())

        self.import_pdf = QtWidgets.QAction(self.main_window)
        self.import_pdf.setObjectName("import_pdf")
        self.clear_records = QtWidgets.QAction(self.main_window)
        self.clear_records.setObjectName("clear_records")
        self.ocr = QtWidgets.QAction(self.main_window)
        self.ocr.setObjectName("ocr")

        self._generate_history_actions()
        self._set_sizebar()  # 设置字号的action和triggered

        self.menu_1.addAction(self.import_pdf)
        self.menu_1.addAction(self.menu_3.menuAction())
        self.menu_2.addAction(self.clear_records)
        self.menu_2.addAction(self.ocr)
        self.menu_2.addAction(self.menu_4.menuAction())

        # 关于信号的操作
        self.signals = self.main_window.signals
        self.signals.ocr_status.connect(self.statusbar_msg)

        self.import_pdf.triggered.connect(self._import_pdf)
        self.clear_records.triggered.connect(self._clear_records)
        self.ocr.triggered.connect(self._begin_ocr)

        self.retranslateUi()  # 重命名action的显示名字

        self.main_window.setMenuBar(self.menubar)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def statusbar_msg(self, filename, status):
        if status == 'ok':
            self.statusbar.showMessage(filename + " OCR完成")
            # self.statusbar.hide()
        else:
            self.statusbar.show()
            self.statusbar.showMessage(filename + status)

    def set_statusbar(self):
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        self.statusbar.hide()

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
            if total < CONST.history_settings.history_file_number:  # 该常量默认为10
                # 如果大于上一次历史记录的数量且小于10，那么代表导入了新的pdf，需要创建新action
                # todo: 如果以后需要重新涉及到PyQt5的话，顺便找一下有没有内置自动更新的button
                exec(
                    f"self.file{total - 1} = QtWidgets.QAction(self.main_window)",
                    self.symbols)
                eval(f"self.menu_3.addAction(self.file{total - 1})")
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

    def _set_sizebar(self):
        # 设置字号栏
        # https://stackoverflow.com/questions/47044129/nameerror-name-self-is-not-defined-after-using-eval
        for i in CONST.menubar_settings.font_size_range:
            exec(
                f"self.size{i} = QtWidgets.QAction(self.main_window)",
                self.symbols)
            eval(f"self.size{i}.setObjectName('size{i}')")
            eval(
                f"self.size{i}.triggered.connect(lambda:self._change_font_size({i}))",
                self.symbols)
            eval(
                f"self.size{i}.setText(_translate('MainWindow', '{i}'))",
                self.symbols)
            eval(f"self.menu_4.addAction(self.size{i})")

    def _get_file_path(self):
        file_path, file_type = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        return file_path

    def _import_pdf(self):
        file_path = self._get_file_path()
        if file_path:
            """判断是否点击了cancel，如果cancel则不切换pdf"""
            # print(fileType)
            self.signals.change_pdf.emit(file_path)
            self._update_history_actions(file_path)  # 导入新pdf更新历史记录
            # self.generate_latest_action.emit(file_name)

    def _change_pdf(self, pdf):
        self.signals.change_pdf.emit(pdf)
        self._update_history_actions(pdf)  # 切换pdf更新历史记录

    def _clear_records(self):
        self.main_window.sentence_query_records.clear()
        # 此时只要再查询一次，历史文件就会被刷新，所以注释了下面的语句，有需要再uncomment
        self.main_window.translation_sentence = ''
        # self.main_window.history_files.update_sentence_records('') # 更新历史文件

    def _begin_ocr(self):
        file_path = self._get_file_path()
        # 估算预计完成时间
        filename, status = self._expected_OCR_time(file_path)
        self.signals.ocr_status.emit(filename, status)

        ocr_process = Process(target=self._ocr, args=(file_path,))
        ocr_process.start()

    def _detection_ocr_achieved(self):
        while True:
            file_path, status = self.OCR_queue.get()
            filename = os.path.basename(file_path)
            self.signals.ocr_status.emit(filename, status)

    def _expected_OCR_time(self, file_path):
        pdfFileObj = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        expected_time = pdfReader.numPages * 2.5
        t = expected_time
        if t // 3600:
            status_msg = " 预计将在{:.0f}小时{:.0f}分钟{:.0f}秒后完成OCR".format(
                t // 3600, t // 60, t % 60)
        elif t // 60:
            status_msg = " 预计将在{:.0f}分钟{:.0f}秒后完成OCR".format(t // 60, t % 60)
        else:
            status_msg = " 预计将在{:.0f}秒后完成OCR".format(t % 60)

        filename = os.path.basename(file_path)

        return filename, status_msg

    def _ocr(self, file_path, ):
        if file_path:
            # 备份文件
            backup_file = file_path + ".backup"
            shutil.copy(file_path, backup_file)
            ok = ocrmypdf.ExitCode.ok  # ocr成功的返回值
            return_code = ocrmypdf.ocr(
                file_path,
                file_path,
                optimize=3,
                use_threads=True,
                output_type='pdf',
                force_ocr=True,
                progress_bar=True)  # in place

            if return_code == ok:
                self.OCR_queue.put((file_path, 'ok'))

    def _change_font_size(self, size):
        self.main_window.translated_text.setStyleSheet(f"font: {size}pt")
        self.main_window.sentence_query_records.setStyleSheet(f"font: {size}pt")

    def retranslateUi(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.menu_1.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "最近打开"))
        self.menu_4.setTitle(_translate("MainWindow", "更改字号"))
        self.import_pdf.setText(_translate("MainWindow", "打开 PDF"))
        self.clear_records.setText(_translate("MainWindow", "清空历史查询"))
        self.ocr.setText(_translate("MainWindow", "OCR"))

        self.import_pdf.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.clear_records.setShortcut(_translate("MainWindow", "Ctrl+l"))
