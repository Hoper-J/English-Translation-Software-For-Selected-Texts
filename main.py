import datetime
import queue
import sys
import threading

from PyQt5.QtCore import Qt
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
        self.signals = MutiSignal()  # 定义了 鼠标selected / 翻译完成 / PDF切换 / OCR状态 信号
        self.raw_queue = queue.Queue()  # 用于翻译线程
        self._init()  # 设置主界面
        self.translation_sentence = self.pdfViewer.records  # 获取初始化后打开的PDF的历史记录
        self.translation_word = ''
        self.update_text()

    def _init(self):
        self.setWindowTitle("论文划线翻译")
        # self.setWindowIcon(QIcon("./image/logo.ico"))

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

        self.translated_text = QPlainTextEdit()
        self.translated_text.setObjectName('translated_text')
        self.sentence_query_records = QPlainTextEdit()
        self.sentence_query_records.setObjectName('sentence_query_records')
        self.word_query_records = QPlainTextEdit()
        self.word_query_records.setObjectName('word_query_records')

        translation_window = QVBoxLayout()
        translation_window.addWidget(self.translated_text)
        translation_window.setContentsMargins(0, 0, 0, 0)  # 设置文本框边缘贴近整个窗口
        tab1.setLayout(translation_window)

        sentence_window = QVBoxLayout()
        sentence_window.addWidget(self.sentence_query_records)
        sentence_window.setContentsMargins(0, 0, 0, 0)
        tab2.setLayout(sentence_window)

        words_window = QVBoxLayout()
        words_window.addWidget(self.word_query_records)
        words_window.setContentsMargins(0, 0, 0, 0)
        tab3.setLayout(words_window)

        vbox = QVBoxLayout()
        vbox.addWidget(tab)

        gbox = QGroupBox()
        gbox.setLayout(vbox)

        # 插入 pdf 阅读器
        self.pdfViewer = PdfViewer(self)
        self.pdfViewer.setContentsMargins(0, 0, 0, 0)
        gbox.setContentsMargins(0, 0, 0, 0)

        # 将pdf和翻译放进垂直布局的box中，并使其可通过中间的Splitter修改左右窗口大小
        hbox = QHBoxLayout()
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.pdfViewer)
        splitter1.addWidget(gbox)
        hbox.addWidget(splitter1)
        widget = QWidget()
        widget.setLayout(hbox)

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
            raw_text = self.raw_queue.get()

            # en_to_zh 是一个 property
            self.translator.en_to_zh = raw_text
            self.signals.translation_completed.emit(self.translator.en_to_zh)

    def to_text_box(self, translation_results=''):
        """将 translation_results 打印到翻译文本框"""
        self.translated_text.setPlainText(translation_results)
        if translation_results[0] == '英':
            # 通过判断翻译处理结果的首个词是否为 英，来判断是否是单词
            self.translation_word += f"{self.selected_text}\n{translation_results}\n"
            self.word_query_records.appendPlainText(self.translation_word)
        else:
            # 设置句子的展现格式
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %X')
            self.html_str = f"""
                        <b>[{now_time}]</b><br>
                        {CONST.main_window.text_format_en}
                        {self.selected_text}
                        </span><br><br>
                        {translation_results}<br>
                    """
            self.translation_sentence += self.html_str
            self.sentence_query_records.appendHtml(self.html_str)
        # self.no_style_str = f"[{now_time}]\n{self.selected_text}\n\n{translation_results}\n"
        # self.translation_sentence += self.no_style_str
        # self.sentence_query_records.appendPlainText(self.no_style_str)

        # todo : 分离翻译和历史记录的保存流程，创建一个线程每隔一段时间自动保存历史记录 或者 采取更好的方法
        self.history_files.update_sentence_records(self.translation_sentence)
        self.history_files.update_word_records(self.translation_word)

    def to_change_pdf(self, pdf):
        """执行切换PDF后的操作"""
        self.history_files.update_recent_open_file(pdf)
        self.pdfViewer.reload_pdf(pdf)
        self.translation_sentence = self.pdfViewer.records  # 随着PDF的切换，更新查询记录
        # self.history_files.update_recent_open_file(pdf) # 这里不记得该不该注释了，故暂不删除，如果最近打开有bug取消注释
        # print(self.history_file.files)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # 设置菜单栏
    menu_bar = MenuBar(main_window)
    main_window.show()

    sys.exit(app.exec_())
