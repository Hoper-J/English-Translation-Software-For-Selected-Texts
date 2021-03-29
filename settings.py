class Settings():
    '''一些样式设置'''
    def __init__(self):
        self.styleSheet = """

            QMainWindow{
                background-image: url("./images/background_.png");
            }

            QTabWidget::pane{
                top:-1px;
                border: none;
            }
            
            
            QTabBar::tab {
              background: rgb(230, 230, 230); 
              border: 1px solid lightgray; 
              padding: 10px;
            } 
            
            QTabBar::tab:selected { 
              background: rgb(245, 245, 245); 
              margin-bottom: -1px; 
            }
             

            #notes_content{
                border-radius: 12px 12px 0 0;
            }
            
            QSplitter:handle{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:4, y2:0, 
                    stop:0 rgba(255, 255, 255, 0), 
                    stop:0.407273 rgba(200, 200, 200, 255), 
                    stop:0.4825 rgba(101, 104, 113, 235), 
                    stop:0.6 rgba(255, 255, 255, 0));
                image: url("./images/splitter_16.png");
     
            }
            QSplitter:handle:hover{
                background-color: rgb(200, 100, 100);
            }
            QSplitter::handle:pressed{
                background-color: rgb(70, 70, 70);
            }
            
            
        """

