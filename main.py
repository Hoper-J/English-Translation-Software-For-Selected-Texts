"""


"""

import datetime
import queue
import sys
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from func_source.history_files import HistoryFiles
from func_source.mutisignal import MutiSignal
from func_source.translator import Translator

from layout_source.menubar import MenuBar
from layout_source.pdfviewer import PdfViewer
from layout_source.settings import Settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history_files = HistoryFiles()
        self.translator = Translator()  # property
        self.signals = MutiSignal()  # 定义了 鼠标release 以及 翻译完成 信号
        self.raw_queue = queue.Queue()  # 用于翻译线程
        self._init()
        self.translation_records = self.pdfViewer.records # 获取查询的历史记录
        self.update_text()
        # self.update_history_file()

    def _init(self):
        self.setWindowTitle("论文划线翻译")
        self.setWindowIcon(QIcon("./image/logo.ico"))

        # 以下为界面 UI
        tab = QTabWidget()
        tab.setMinimumWidth(2)

        tab1 = QTabBar()
        tab2 = QTabBar()
        tab.addTab(tab1, "译文")
        tab.addTab(tab2, "历史查询")
        tab1.setObjectName('tab1')
        tab2.setObjectName('tab2')

        self.query_history_records = QPlainTextEdit()
        self.query_history_records.setObjectName('query_history_records')

        self.translate_text = QPlainTextEdit()
        self.translate_text.setObjectName('translate_text')

        translate_layout = QVBoxLayout()
        translate_layout.addWidget(self.translate_text)
        translate_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本框边缘贴近整个窗口
        tab1.setLayout(translate_layout)

        records_layout = QVBoxLayout()
        records_layout.addWidget(self.query_history_records)
        records_layout.setContentsMargins(0, 0, 0, 0)
        tab2.setLayout(records_layout)

        # 设置样式
        self.styleSheet = Settings().styleSheet
        self.setStyleSheet(self.styleSheet)

        # self.filter = TextFilter()
        vbox = QVBoxLayout()
        vbox.addWidget(tab)

        gbox = QGroupBox()
        gbox.setStyleSheet("font: 12pt")
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

        self.signals.mouse_selected.connect(self.get_text)
        self.signals.translation_completed.connect(self.to_text_box)

        self.signals.change_pdf.connect(self.to_change_pdf)

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
            # before = time.time()
            self.translator.en_to_zh = raw_text
            # after = time.time()
            # print(after-before)
            # pyqt5不允许在非主线程中使用信号槽
            self.signals.translation_completed.emit(self.translator.en_to_zh)

    def to_text_box(self, str=''):
        """将 str 打印到翻译文本框"""
        self.translate_text.setPlainText(str)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %X')
        self.html_str = f"""
                    <b>[{now_time}]</b><br>
                    <span style = "font-size: 14pt; font-family: Times New Roman;">
                    {self.selected_text}
                    </span><br><br>
                    {str}<br>
                """
        self.translation_records += self.html_str
        self.query_history_records.appendHtml(self.html_str)

        # self.no_style_str = f"[{now_time}]\n{self.selected_text}\n\n{str}\n"
        # self.translation_records += self.no_style_str
        # self.query_history_records.appendPlainText(self.no_style_str)

        self.history_files.update_records(self.translation_records)

    def to_change_pdf(self, pdf):
        self.pdfViewer.reload_pdf(pdf)
        self.translation_records = self.pdfViewer.records
        self.history_files.store_file(pdf)
        # print(self.history_file.files)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # 设置菜单栏
    menu_bar = MenuBar(main_window)
    # menu_bar.set_menubar()
    main_window.show()
    sys.exit(app.exec_())
