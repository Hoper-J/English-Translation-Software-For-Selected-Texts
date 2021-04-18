import datetime
import multiprocessing
import os
import queue
import shutil
import sys
import threading

import PyPDF2
import ocrmypdf
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from const import CONST
from function.history_files import HistoryFiles
from function.mutisignal import MutiSignal
from function.translator import Translator
from layout.menubar import MenuBar
from layout.pdfviewer import PdfViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history_files = HistoryFiles()
        self.translator = Translator()  # property
        self.signals = MutiSignal()  # 定义了 鼠标release 以及 翻译完成 信号
        self.raw_queue = queue.Queue()  # 用于翻译线程
        self._init()
        self.translation_records = self.pdfViewer.records # 获取查询的历史记录
        self.word_records = ''
        self.update_text()
        # self.update_history_file()
    def _init(self):
        self.setWindowTitle("论文划线翻译")
        self.setWindowIcon(QIcon("./image/logo.ico"))

        # 以下为界面 UI
        tab = QTabWidget()
        tab.setMinimumWidth(3)

        tab1 = QTabBar()
        tab2 = QTabBar()
        tab3 = QTabBar()
        tab.addTab(tab1, "译文")
        tab.addTab(tab2, "历史查询")
        tab.addTab(tab3, "单词记录")
        tab1.setObjectName('tab1')
        tab2.setObjectName('tab2')
        tab3.setObjectName('tab3')

        self.translate_text = QPlainTextEdit()
        self.translate_text.setObjectName('translate_text')
        self.history_query = QPlainTextEdit()
        self.history_query.setObjectName('history_query')
        self.word_record = QPlainTextEdit()
        self.word_record.setObjectName('word_record')

        translate_layout = QVBoxLayout()
        translate_layout.addWidget(self.translate_text)
        translate_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本框边缘贴近整个窗口
        tab1.setLayout(translate_layout)

        records_layout = QVBoxLayout()
        records_layout.addWidget(self.history_query)
        records_layout.setContentsMargins(0, 0, 0, 0)
        tab2.setLayout(records_layout)

        words_layout = QVBoxLayout()
        words_layout.addWidget(self.word_record)
        words_layout.setContentsMargins(0, 0, 0, 0)
        tab3.setLayout(words_layout)

        vbox = QVBoxLayout()
        vbox.addWidget(tab)

        gbox = QGroupBox()
        # gbox.setStyleSheet("font: 12pt")
        gbox.setLayout(vbox)

        # 插入 pdf 阅读器
        self.pdfViewer = PdfViewer(self)
        self.pdfViewer.setContentsMargins(0, 0, 0, 0)
        gbox.setContentsMargins(0, 0, 0, 0)

        # 将pdf和翻译放进垂直布局的box中，并使其可通过中间的Splitter修改左右窗口大小
        hBoxLayout = QHBoxLayout()
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.pdfViewer)
        splitter1.addWidget(gbox)
        hBoxLayout.addWidget(splitter1)
        widget = QWidget()
        widget.setLayout(hBoxLayout)

        self.setCentralWidget(widget)
        self.recent_text = ""
        self.showMaximized()

        # 设置样式
        self.styleSheet = CONST.main_window.style_sheet
        self.setStyleSheet(self.styleSheet)

        self.signals.mouse_selected.connect(self.get_text)
        self.signals.translation_completed.connect(self.to_text_box)

        self.signals.change_pdf.connect(self.to_change_pdf)
        # self.signals.ocr_pdf.connect(self.to_ocr_pdf)


    def get_text(self):
        """将选中的文本加入未处理文本的"消费者"队列（raw_queue）"""
        if self.pdfViewer.hasSelection():
            # 当前if语句是为了确定鼠标事件发生在pdfViewer中
            self.selected_text = self.pdfViewer.selectedText()
            # print(selected_text)

            self.raw_queue.put(self.selected_text)

    def update_text(self):
        """
        生成线程处理翻译
        线程完成翻译时将触发文本更新信号
        """
        thread_translate = threading.Thread(target=self.translate,
                                            args=())
        thread_translate.start()

        # 信号 selectionChanged 太"灵敏"了，不建议使用，其在鼠标未松开时依然一直触发
        # self.pdfViewer.selectionChanged.connect(self.get_text)

    # def update_history_file(self):
    #     while True:
    #         self.update_history_queue.get()
    #
    #         pass

    def translate(self):
        """返回翻译的内容"""
        while True:
            # en_to_zh 是一个 property
            raw_text = self.raw_queue.get()
            self.translator.en_to_zh = raw_text
            self.signals.translation_completed.emit(self.translator.en_to_zh)

    def to_text_box(self, str=''):
        """将 str 打印到翻译文本框"""
        # todo : 分离翻译和历史记录保存，创建一个线程每隔一段时间自动保存历史记录
        self.translate_text.setPlainText(str)
        if str[0] == '英':
            # 通过判断翻译处理结果的首个词是否为 英，来判断是否是单词
            self.word_records += f"{self.selected_text}\n{str}\n"
            self.word_record.appendPlainText(self.word_records)
        else:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %X')
            self.html_str = f"""
                        <b>[{now_time}]</b><br>
                        <span style = "font-size: 14pt; font-family: Times New Roman;">
                        {self.selected_text}
                        </span><br><br>
                        {str}<br>
                    """
            self.translation_records += self.html_str
            self.history_query.appendHtml(self.html_str)
        # self.no_style_str = f"[{now_time}]\n{self.selected_text}\n\n{str}\n"
        # self.translation_records += self.no_style_str
        # self.history_query.appendPlainText(self.no_style_str)

        self.history_files.update_records(self.translation_records)
        self.history_files.update_word(self.word_records)

    def to_change_pdf(self, pdf):
        self.history_files.store_file(pdf)
        self.pdfViewer.reload_pdf(pdf)
        self.translation_records = self.pdfViewer.records
        self.history_files.store_file(pdf)
        # print(self.history_file.files)

    def to_ocr_pdf(self, statusbar):
        ocr_process = multiprocessing.Process(target=self._ocr, args=(statusbar,))
        ocr_process.start()

    def _ocr(self, statusbar):
        file_path, file_type = QFileDialog.getOpenFileName(
            self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")

        if file_path:
            # 备份文件
            backup_file = file_path + ".backup"
            shutil.copy(file_path, backup_file)

            OK = 'ExitCode.ok'  # ocr成功的返回值
            # dirpath, filename = os.path.split(filepath)

            # before = time.time()
            # 估算预计完成时间
            pdfFileObj = open(file_path, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            expected_time = pdfReader.numPages * 2.5
            t = expected_time
            if t // 3600:
                status_msg = "预计将在{:.0f}小时{:.0f}分钟{:.0f}秒后完成OCR".format(t // 3600, t // 60, t % 60)
            elif t // 60:
                status_msg = "预计将在{:.0f}分钟{:.0f}秒后完成OCR".format(t // 60, t % 60)
            else:
                status_msg = "预计将在{:.0f}秒后完成OCR".format(t % 60)

            filename = os.path.basename(file_path)

            # 状态栏提示信息
            statusbar.show()
            statusbar.showMessage(filename + status_msg)

            # OCR
            return_code = ocrmypdf.ocr(file_path, file_path,
                                            optimize=3, use_threads=True, output_type='pdf', force_ocr=True,
                                            progress_bar=True)  # in place
            # after = time.time()
            # print(after-before)
            if self.return_code == OK:

                status_msg = f"OCR {filename} 已经完成"
                self.statusbar.showMessage(status_msg)
                print("完成")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # 设置菜单栏
    menu_bar = MenuBar(main_window)
    main_window.show()
    sys.exit(app.exec_())
