'''
Author: your name
Date: 2021-04-05 10:19:25
LastEditTime: 2021-04-06 20:12:22
LastEditors: your name
Description: In User Settings Edit
FilePath: /my_translation/func_source/history_file.py
'''
import os
import shelve

from my_translation.const import CONST


class HistoryFiles:
    def __init__(self):
        current_dir = os.path.split(os.path.realpath(__file__))[0]
        self.file_path = os.path.join(
            os.path.dirname(current_dir), 'history_data.dat')
        self.history_dt = shelve.open(self.file_path)

        self.files = [] # 将初始化定义移上来，可以省略finally中的操作
        self.word_record = ''

        # todo: 对于移动了的文件的历史记录在报错后删除
        try:
            # shelve.open的返回并不是普通映射，应该用副本来修改值
            self.files = self.history_dt['filenames']
            self.word_record = self.history_dt['word_record']
        except KeyError:
            self.history_dt['filenames'] = self.files
            self.history_dt['word_record'] = self.word_record
        # finally:
        #     self.files = self.history_dt['filenames']
            # self.files.reverse()  # 历史记录应为倒序

        self.records = ''

        self.current_file = self.get_latest_file()

    def store_file(self, filename):
        """记录历史 (<=10)，超过后删除最早的历史"""
        if len(self.files) >= CONST.history_settings.history_file_number:
            del self.files[-1]
        try:
            self.files.remove(filename)
        except ValueError:
            pass
        finally:
            self.files.insert(0, filename)
            self._update_database()

    def get_latest_file(self):
        """返回最近一次打开的pdf，如果第一次打开，则返回readme.pdf"""
        try:
            return self.files[0]
        except IndexError:
            return CONST.history_settings.initial_file


    def get_records(self, filename):
        """获取当前文件的查询记录"""
        self.current_file = filename
        try:
            self.records = self.history_dt[filename]
        except KeyError:
            self.history_dt[filename] = ''
            self.records = ''

        return self.records

    def update_records(self, str):
        self.records = str
        self._update_database() # store_file和当前函数有冗余调用，todo:优化

        # self.history_dt.close()
        # self.history_dt = shelve.open(self.file_path)  # 再次打开为了下次存储，但是应当有更简单的方法


    def update_word(self, str):
        self.word_record = str
        self._update_database()


    def _update_database(self):
        """保存"""
        self.history_dt['filenames'] = self.files # list(reversed(self.files))
        self.history_dt[self.current_file] = self.records
        self.history_dt['word_record'] = self.word_record
        self.history_dt.close()
        self.history_dt = shelve.open(self.file_path)  # 再次打开为了下次存储，但是应当有更简单的方法

