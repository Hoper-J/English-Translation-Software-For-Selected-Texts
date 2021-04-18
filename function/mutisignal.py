from PyQt5.QtCore import QObject, pyqtSignal


class MutiSignal(QObject):
    mouse_selected = pyqtSignal()
    translation_completed = pyqtSignal(str)
    change_pdf = pyqtSignal(str)
    ocr_status = pyqtSignal(str, str)
