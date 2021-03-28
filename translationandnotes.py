from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import *


class TranslationAndNotes():
    def __init__(self):
        self.tab = QTabWidget()
        self.tab.setMinimumWidth(2)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab.addTab(self.tab1, "译文")
        self.tab.addTab(self.tab2, "笔记")


        self.notebook = QPlainTextEdit()
        self.notebook.setStyleSheet("font: 12pt")

        self.translate_result = QPlainTextEdit()
        self.translate_result.setStyleSheet("font: 12pt")

        translate_content = QVBoxLayout()
        translate_content.addWidget(self.translate_result)
        translate_content.setContentsMargins(0, 0, 0, 0)  # 设置距离左上右下的距离
        self.tab1.setLayout(translate_content)

        noterbook_content = QVBoxLayout()
        noterbook_content.addWidget(self.notebook)
        noterbook_content.setContentsMargins(0, 0, 0, 0)  # 设置距离左上右下的距离
        self.tab2.setLayout(noterbook_content)

        self.set_style_sheet()

    def set_style_sheet(self):
        # self.tab1.setStyleSheet('background-color:black;')
        # self.translate_result.setStyleSheet('background-color:yellow;')
        pass


