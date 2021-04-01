'''
Author: your name
Date: 2021-03-29 16:51:14
LastEditTime: 2021-03-31 16:38:58
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /my_translation/func_source/underlined_text.py
'''
import logging
import threading
import queue
import time

from .translator import Translator

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)


class TrackMouse:
    def __init__(self,pdfViewer, translate_text):
        self.raw_string = ''
        self.translator = Translator()
        self.raw_queue = queue.Queue()
        self.last_text = ''
        mouse_track = threading.Thread(target=self.get_selection,
                        args=(pdfViewer,))
        mouse_track.start()

        auto_translate = threading.Thread(target=self.translate,
                                          args=(translate_text,))
        auto_translate.start()

    def get_selection(self, pdfViewer):
        # todo: 创建线程跟踪鼠标
        while True:
            if pdfViewer.hasSelection():
                selected_text = pdfViewer.selectedText()
                if self.last_text != selected_text:
                    self.last_text = selected_text
                    print(self.last_text)
                    self.raw_queue.put(self.last_text)
                time.sleep(0.1) # 切换线程


    def translate(self, translate_text):
        """返回翻译的内容"""
        while True:
            # en_to_zh 是一个 property
            raw_text = self.raw_queue.get()
            self.translator.en_to_zh = raw_text
            translate_text.setPlainText(self.translator.en_to_zh)




