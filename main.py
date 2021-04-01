"""
感觉下划线命名在导入PyQt5后显得格格不入，故以下变量一致采用小驼峰命名


"""


import sys
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from layout_source.menubar import MenuBar
from layout_source.settings import Settings
from layout_source.pdfviewer import PdfViewer

from func_source.track_mouse import TrackMouse

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initui()
        self.update_text()
        # todo: 创建线程获取翻译
        # self.thread_my = WatchClip()
        # self.thread_my.start()

    def update_text(self):
        tracker = TrackMouse(self.pdfViewer,self.translate_text)
        # mouce_track = threading.Thread(target=tracker.get_selection,
        #                  args=(self.pdfViewer,))
        # mouce_track.start()
        #
        # auto_translate = threading.Thread(target=tracker.translate,
        #                                   args=(self.translate_text,))
        # auto_translate.start()
        # 信号 selectionChanged 太"灵敏"了，不建议使用，其在鼠标未松开时依然一直触发
        # self.pdfViewer.selectionChanged.connect(self.printt)
    #     if self.pdfViewer.hasSelection():
    #         self.printt()
    # def printt(self):
    #     print(self.pdfViewer.selectedText())
    def initui(self):
        self.setWindowTitle("论文划线翻译")
        self.setWindowIcon(QIcon("./image/logo.ico"))
        tab = QTabWidget()
        tab.setMinimumWidth(2)

        tab1 = QTabBar()
        tab2 = QTabBar()
        tab.addTab(tab1, "译文")
        tab.addTab(tab2, "笔记")
        tab1.setObjectName('tab1')
        tab2.setObjectName('tab2')

        self.notes_content = QPlainTextEdit()
        self.notes_content.setStyleSheet("font: 12pt")
        self.notes_content.setObjectName('notes_content')

        self.translate_text = QPlainTextEdit()
        self.translate_text.setStyleSheet("font: 12pt")
        self.translate_text.setObjectName('translate_text')


        translate_layout = QVBoxLayout()
        translate_layout.addWidget(self.translate_text)
        translate_layout.setContentsMargins(0, 0, 0, 0)  # 设置文本框边缘贴近整个窗口
        tab1.setLayout(translate_layout)


        noterbook_layout = QVBoxLayout()
        noterbook_layout.addWidget(self.notes_content)
        noterbook_layout.setContentsMargins(0, 0, 0, 0)
        tab2.setLayout(noterbook_layout)

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
        self.pdfViewer = PdfViewer()
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





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # 设置菜单栏
    menu_bar = MenuBar()
    menu_bar.set_menubar(main_window)

    main_window.show()
    sys.exit(app.exec_())
