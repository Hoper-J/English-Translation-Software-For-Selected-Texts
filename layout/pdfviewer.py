from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView

from my_translation.const import CONST


class PdfViewer(QWebEngineView):
    def __init__(self, MainWindow):
        super().__init__()
        self._glwidget = None
        self.history_dt = MainWindow.history_files
        self.records = ''
        self.query_history_records = MainWindow.sentence_query_records

        self.word_record = MainWindow.word_query_records
        self.word_records = self.history_dt.word_record
        self.word_record.setPlainText(self.word_records)

        pdf = self.history_dt.current_file

        self.reload_pdf(pdf)

        self.mouse_selected = MainWindow.signals.mouse_selected

        self.installEventFilter(self)

    def reload_pdf(self, pdf):
        """导入其他pdf"""
        PDFJS = CONST.pdf_settings.js_path
        self.load(
            QtCore.QUrl.fromUserInput(
                '%s?file=%s' %
                (PDFJS, pdf)))

        self.records = self.history_dt.get_records(pdf)
        self.query_history_records.clear()
        # self.sentence_query_records.setPlainText(self.records)
        self.query_history_records.appendHtml(self.records)

    def _get_file_qurl(self, file_path):
        file_qurl = QtCore.QUrl.fromLocalFile(file_path)
        return QtCore.QUrl.toString(file_qurl)

    def event(self, e):
        """
        Detect child add event, as QWebEngineView do not capture mouse event directly,
        the child layer _glwidget is implicitly added to QWebEngineView and we track mouse event through the glwidget
        :param e: QEvent
        :return: super().event(e)
        """
        if self._glwidget is None:
            if e.type() == QEvent.ChildAdded and e.child().isWidgetType():
                self._glwidget = e.child()
                self._glwidget.installEventFilter(self)
        return super().event(e)

    # def mouseReleaseEvent(self, event):
    #     self.mouse_selected.emit()
    #     super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        """
        捕获鼠标抬起事件失败的解决方法：
        https://stackoverflow.com/questions/50887951/pyqt4-mouse-release-event-not-working
        """
        if event.type() == (
                QEvent.MouseButtonRelease):  # 我记得之前双击是奏效的，不知为何今天无法奏效 | QEvent.MouseButtonDblClick):
            self.mouse_selected.emit()

        return super().eventFilter(obj, event)

