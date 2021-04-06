import os
import shelve


class HistoryFile:
    def __init__(self):
        current_dir = os.path.split(os.path.realpath(__file__))[0]
        self.file_path = os.path.join(
            os.path.dirname(current_dir), 'files.dat')
        self.history_dt = shelve.open(self.file_path)
        try:
            # shelve.open的返回并不是普通映射，应该用副本来修改值
            self.files = self.history_dt['filenames']
        except KeyError:
            self.history_dt['filenames'] = []
        finally:
            self.files = self.history_dt['filenames']
            self.files.reverse()  # 历史记录应为倒序

    def store_file(self, filename):
        """记录历史 (<=10)，超过后删除最早的历史"""
        if len(self.files) >= 10:
            del self.files[-1]
        try:
            self.files.remove(filename)
        except ValueError:
            pass
        finally:
            self.files.insert(0, filename)
            self._update_database()

    def get_latest_file(self):
        return self.files[0]

    def _update_database(self):
        """保存"""
        self.history_dt['filenames'] = list(reversed(self.files))
        self.history_dt.close()
        self.history_dt = shelve.open(self.file_path)  # 再次打开为了下次存储，但是应当有更简单的方法
