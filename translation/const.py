import os

from functools import wraps


def Const(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise Exception('const : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls


@Const
class _HistoryFiles(object):
    history_file_number = 10  # 历史文件记录上限
    initial_file = os.path.abspath("../file/readme.pdf")


@Const
class _PdfViewer(object):
    # 'file:///Users/home/PycharmProjects/pythonProject1/Translation/pdfjs/web/new_viewer.html'
    js_path = "file://" + os.path.abspath("../pdfjs/web/viewer.html")


@Const
class _MainWindow(object):
    text_format_en = '<span style = "font-size: 14pt; font-family: Times New Roman;">'  # 历史查询中英文文本的格式
    style_sheet = """

                /* QMainWindow{
                    background-image: url("./images/background_.png");
                } */


                /* 右侧窗体布局 */
                QTabWidget::pane {
                    border: 1px solid black;
                    background: white;
                }
                QTabWidget::tab-bar:top {
                    top: 1px;
                }
                QTabWidget::tab-bar:bottom {
                    bottom: 1px;
                }
                QTabWidget::tab-bar:left {
                    right: 1px;
                }
                QTabWidget::tab-bar:right {
                    left: 1px;
                }
                QTabBar::tab {
                    border: 1px solid black;
                    background: rgb(230, 230, 230);
                }
                QTabBar::tab:selected {
                    background: white;
                    margin-bottom: -1px;
                }
                QTabBar::tab:!selected {
                    background: silver;
                }
                QTabBar::tab:!selected:hover {
                    background: #999;
                }
                QTabBar::tab:top:!selected {
                    margin-top: 3px;
                }
                QTabBar::tab:bottom:!selected {
                    margin-bottom: 3px;
                }
                QTabBar::tab:top, QTabBar::tab:bottom {
                    min-width: 8ex;
                    margin-right: -1px;
                    padding: 5px 10px 5px 10px;
                }
                QTabBar::tab:top:last, QTabBar::tab:bottom:last,
                QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
                    margin-right: 0;
                }
                QTabBar::tab:left:!selected {
                    margin-right: 3px;
                }
                QTabBar::tab:right:!selected {
                    margin-left: 3px;
                }
                QTabBar::tab:left, QTabBar::tab:right {
                    min-height: 8ex;
                    margin-bottom: -1px;
                    padding: 10px 5px 10px 5px;
                }


                QSplitter:handle{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 255, 255, 0),
                        stop:0.407273 rgba(200, 200, 200, 255),
                        stop:0.4825 rgba(101, 104, 113, 235),
                        stop:0.6 rgba(255, 255, 255, 0));


                }

                QSplitter::handle:pressed{
                    background-color: rgb(127, 127, 127);
                }


            """


@Const
class _MenuBar(object):
    font_size_range = range(10, 16)  # 字号范围 10-15


@Const
class _Const(object):
    main_window = _MainWindow()
    history_settings = _HistoryFiles()
    pdf_settings = _PdfViewer()
    menubar_settings = _MenuBar()


CONST = _Const()
