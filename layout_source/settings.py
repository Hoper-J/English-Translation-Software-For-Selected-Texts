class Settings():
    '''一些样式设置'''
    def __init__(self):
        self.styleSheet = """

            QMainWindow{
                background-image: url("./images/background_.png");
            }


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

