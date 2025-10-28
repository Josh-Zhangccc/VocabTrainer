import pandas as pd
from  data_manager import *
from utils import df
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                               QPushButton, QLabel, QVBoxLayout, 
                               QLineEdit,QWidget,QMessageBox)



class MainWindow(QMainWindow):
    def __init__(self,df):
        super().__init__()
        self.df=Data(df)
        self.series=None
        self.setWindowTitle('主页')
        self.setGeometry(250,150,1000,725)

        #组件放置
        self.start_button=QPushButton('开始学习',self)
        self.next_button=QPushButton('Next',self)
        self.show_details_button=QPushButton('显示详细',self)
        self.label_word=QLabel('')
        self.label_details=QLabel('')
        self.search_input=QLineEdit()
        self.search_input.setPlaceholderText('You can search words here')
        self.back_button=QPushButton('')

        #布局
        layout=QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.label_word)
        layout.addWidget(self.next_button);self.next_button.setVisible(False)
        layout.addWidget(self.back_button);self.back_button.setVisible(False)
        layout.addWidget(self.show_details_button);self.show_details_button.setVisible(False)
        layout.addWidget(self.label_details)
        layout.addWidget(self.search_input);self.search_input.setVisible(False)

        container=QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #链接
        self.start_button.clicked.connect(self.on_click_start_button)
        self.show_details_button.clicked.connect(self.on_cilck_sdb)
        self.next_button.clicked.connect(self.on_click_next_button)
        self.search_input.returnPressed.connect(self.on_submit_clicked)


    def on_click_start_button(self):
        series=self.df.get_random_word()
        word=series['word']
        self.label_word.setText(f'单词：{word}')
        self.start_button.deleteLater()
        self.next_button.setVisible(True)
        self.show_details_button.setVisible(True)
        self.search_input.setVisible(True)

    def on_cilck_sdb(self):
        details=self.df.get_details('all')
        self.label_details.setText(f'详细：{details}')

    
    def on_click_next_button(self):
        self.label_details.setText('')
        self.label_word.setText('')
        series=self.df.get_random_word()
        word=series['word']
        self.label_word.setText(f'单词：{word}')

    def on_submit_clicked(self):
        w = str(self.search_input.text()).strip()
        if not w:
            QMessageBox.warning(self, "提示", "请输入要搜索的单词")
            return

        series=self.df.search_word(w,'first match')
        if series==None:
            self.label_word.setText(f'未找到包含{w}的单词，请确认拼写正确或尝试不同词性')
            self.label_details.setText("")
        else:
            print(series)
            self.label_word.setText(series['word'])
            self.details=self.df.get_details('all')
            self.label_details.setText(self.details)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow(df)
    window.show()
    sys.exit(app.exec())
