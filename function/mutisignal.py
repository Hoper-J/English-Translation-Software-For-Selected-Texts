from PyQt5.QtCore import QObject, pyqtSignal


class MutiSignal(QObject):
    mouse_selected = pyqtSignal()
    translation_completed = pyqtSignal(str)
    change_pdf = pyqtSignal(str)
    ocr_status = pyqtSignal(str, str)
    # generate_latest_action = pyqtSignal(str) # 当用户导入新文件时，添加到历史记录
