import sys

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from menubar import MenuBar
from pdfviewer import PdfViewer
from menubar import MenuBar
from translationandnotes import TranslationAndNotes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("论文划线翻译")
        self.setWindowIcon(QIcon("/Users/home/PycharmProjects/pythonProject1/my_translation/image/logo.ico"))


        # todo: 创建线程获取翻译
        # self.thread_my = WatchClip()
        # self.thread_my.start()

        '''    *****************************  create translation area  ******************************     '''
        # todo: 改成译文和笔记

        self.right_interface = TranslationAndNotes()

        # self.filter = TextFilter()
        vbox = QVBoxLayout()
        vbox.addWidget(self.right_interface.tab)

        gbox = QGroupBox()
        gbox.setStyleSheet("font: 12pt")
        gbox.setLayout(vbox)

        # pdf 设置
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

    qss = '''
        right_interface#tab1{
            background-color: black;
            color: yellow;
            }
    '''
    main_window.setStyleSheet(qss)
    # con.translationChanged.connect(main_window.updateTranslation)
    # con.pdfViewMouseRelease.connect(main_window.updateByMouseRelease)
    # main_window.notebook.textChanged.connect(main_window.updateByTextEdit)
    # main_window.text_size_combobox.currentIndexChanged.connect(main_window.updateOriTextSizeByIndexChanged)
    # main_window.text_size_combobox.currentIndexChanged.connect(main_window.updateResTextSizeByIndexChanged)
    main_window.show()
    sys.exit(app.exec_())
