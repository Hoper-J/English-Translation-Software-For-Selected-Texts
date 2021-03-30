"""
感觉下划线命名在导入PyQt5后显得格格不入，故以下变量一致采用小驼峰命名


"""


import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from layout_source.menubar import MenuBar
from layout_source.settings import Settings
from layout_source.pdfviewer import PdfViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("论文划线翻译")
        self.setWindowIcon(QIcon("./image/logo.ico"))
        # todo: 创建线程获取翻译
        # self.thread_my = WatchClip()
        # self.thread_my.start()

        '''    *****************************  translation/notes area  ******************************     '''

        tab = QTabWidget()
        tab.setMinimumWidth(2)

        tab1 = QTabBar()
        tab2 = QTabBar()
        tab.addTab(tab1, "译文")
        tab.addTab(tab2, "笔记")
        tab1.setObjectName('tab1')
        tab2.setObjectName('tab2')

        notes_content = QPlainTextEdit()
        notes_content.setStyleSheet("font: 12pt")
        notes_content.setObjectName('notes_content')

        translateText = QPlainTextEdit()
        translateText.setStyleSheet("font: 12pt")
        translateText.setObjectName('translateText')

        translateLayout = QVBoxLayout()
        translateLayout.addWidget(translateText)
        translateLayout.setContentsMargins(0, 0, 0, 0)  # 设置距离左上右下的距离
        tab1.setLayout(translateLayout)

        noterbookLayout = QVBoxLayout()
        noterbookLayout.addWidget(notes_content)
        noterbookLayout.setContentsMargins(0, 0, 0, 0)  # 设置距离左上右下的距离
        tab2.setLayout(noterbookLayout)

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

    # main_window.setWindowOpacity(0.6)

    # qss = '''
    #             QPlainTextEdit#translateText("\n"
    #                                        "background-color:black;\n"
    #                                        " \n"
    #                                        "")
    #         '''
    # main_window.setStyleSheet(qss)

    # con.translationChanged.connect(main_window.updateTranslation)
    # con.pdfViewMouseRelease.connect(main_window.updateByMouseRelease)
    # main_window.notes_content.textChanged.connect(main_window.updateByTextEdit)
    # main_window.text_size_combobox.currentIndexChanged.connect(main_window.updateOriTextSizeByIndexChanged)
    # main_window.text_size_combobox.currentIndexChanged.connect(main_window.updateResTextSizeByIndexChanged)
    main_window.show()
    sys.exit(app.exec_())
