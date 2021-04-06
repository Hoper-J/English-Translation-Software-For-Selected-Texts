from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PdfViewer(QWebEngineView):
    def __init__(self, MainWindow):
        super().__init__()
        self._glwidget = None
        self._PDFJS = 'file:///Users/home/PycharmProjects/pythonProject1/my_translation/pdfjs/web/viewer.html'
        try:
            pdf = MainWindow.history_file.files[0]
        except BaseException:
            pdf = '/Users/home/Downloads/2021徐涛核心考案.pdf'
        self.reload_pdf(pdf)
        self.mouse_selected = MainWindow.signals.mouse_selected

        self.installEventFilter(self)

    def reload_pdf(self, pdf):
        """导入其他pdf"""
        self.pdf = pdf
        self.load(
            QtCore.QUrl.fromUserInput(
                '%s?file=%s' %
                (self._PDFJS, self.pdf)))

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
                ###print('child add')
                self._glwidget = e.child()
                self._glwidget.installEventFilter(self)
        return super().event(e)

    def mouseReleaseEvent(self, event):
        self.mouse_selected.emit()
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        """
        捕获鼠标抬起事件失败的解决方法：
        https://stackoverflow.com/questions/50887951/pyqt4-mouse-release-event-not-working
        """
        if event.type() == (QEvent.MouseButtonRelease | QEvent.MouseButtonDblClick):
            self.mouse_selected.emit()

        return super().eventFilter(obj, event)
    # def eventFilter(self, source, event) -> bool:
    #     if event.type() == QEvent.MouseButtonRelease:
    #         self.mouse_selected.emit()
    #     return super().eventFilter(source, event)
