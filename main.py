import pandas as pd
from  data_manager import *
from utils import open
from json_utils import UserManager
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                               QPushButton, QLabel, QVBoxLayout, 
                               QLineEdit,QWidget,QMessageBox,
                               QStatusBar)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from config import DIC


class MainWindow(QMainWindow):
    def __init__(self,user_id:str,dic:str):
        super().__init__()
        self.user_id=user_id
        self.UM=UserManager(self.user_id,dic)
        df=open(dic)
        self.df=Data(df)
        self.series=None
        self.learned=self.UM.output('learned') #list
        self.setWindowTitle('主页')
        self.setGeometry(250,150,1000,725)

        #组件放置
        self.button_start=QPushButton('开始学习',self)
        self.button_next=QPushButton('Next',self)
        self.button_show_details=QPushButton('显示详细',self)
        self.label_word=QLabel('')
        self.label_details=QLabel('')
        self.search_input=QLineEdit()
        self.search_input.setPlaceholderText('You can search words here')
        self.back_button=QPushButton('')

        self.bar=QStatusBar()
        self.setStatusBar(self.bar)
        self.bar.showMessage(f'English Learning Needs Patience \n 当前学习的字典为：{dic}')

        self.create_menus()#创建工具栏，优化搜索与学习之间的显示

        #布局
        layout=QVBoxLayout()
        layout.addWidget(self.search_input);self.search_input.setVisible(False)        
        layout.addWidget(self.button_start)
        layout.addWidget(self.label_word)
        layout.addWidget(self.button_next);self.button_next.setVisible(False)
        layout.addWidget(self.back_button);self.back_button.setVisible(False)
        layout.addWidget(self.button_show_details);self.button_show_details.setVisible(False)
        layout.addWidget(self.label_details)


        container=QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        #链接
        self.button_start.clicked.connect(self.on_click_start_button)
        self.button_show_details.clicked.connect(self.on_cilck_sdb)
        self.button_next.clicked.connect(self.on_click_next_button)
        self.search_input.returnPressed.connect(self.on_submit_clicked)

    def show_search(self):
        self.search_input.setVisible(True)
        self.label_word.setText(None)
        self.label_details.setText(None)
        self.button_next.setVisible(False)
        self.button_show_details.setVisible(False)

    def show_learn(self):
        self.search_input.setVisible(False)
        self.label_details.setVisible(True)
        self.label_word.setVisible(True)
        self.label_details.setText(None)
        self.label_word.setText(None)
        self.button_next.setVisible(True)
        self.button_show_details.setVisible(True)
        

    def on_click_start_button(self):
        series=self.df.get_rw_besides(self.learned)
        word=series['word']
        self.label_word.setText(f'单词：{word}')
        self.button_start.deleteLater()
        self.button_next.setVisible(True)
        self.button_show_details.setVisible(True)
        self.learned.append(series['wordrank']-1)
        self.UM.record_word(series['wordrank']-1,3)#暂时设定为3，后续再改
        self.UM.save_json()
    def on_cilck_sdb(self):
        details=self.df.get_details('all')
        self.label_details.setText(f'详细：{details}')

    
    def on_click_next_button(self):
        self.label_details.setText('')
        self.label_word.setText('')
        series=self.df.get_rw_besides(self.learned)
        word=series['word']
        self.label_word.setText(f'单词：{word}')
        self.learned.append(series['wordrank']-1)
        self.UM.record_word(series['wordrank']-1,3)#暂时设定为3，后续再改
        self.UM.save_json()


    def on_submit_clicked(self):
        w = str(self.search_input.text()).strip()
        if not w:
            QMessageBox.warning(self, "提示", "请输入要搜索的单词")
            return

        series=self.df.search_word(w,'first match')
        if series is None:
            self.label_word.setText(f'未找到包含{w}的单词，请确认拼写正确或尝试不同词性')
            self.label_details.setText("")
        else:
            print(series)
            self.label_word.setText(series['word'])
            self.details=self.df.get_details('all')
            self.label_details.setText(self.details)

    def switch(self,dic:str):
        if dic in DIC:
            if dic !=self.UM.dic_info():
                self.UM=UserManager(self.user_id,dic)
                self.df=Data(open(dic))

                self.label_details.setText("")
                self.label_word.setText("")
            else:
                QMessageBox.information(self,'SWITCH FAILED',f'已经在{dic}目录！')


    def create_menus(self):
        menu_bar=self.menuBar()
        functions=menu_bar.addMenu('功能')

        action_search=QAction('search',self)
        action_search.setShortcut('Ctrl+Shift+s')
        action_search.triggered.connect(self.show_search)

        action_learn=QAction('learn',self)
        action_learn.setShortcuts('Ctrl+Shift+l')
        action_learn.triggered.connect(self.show_learn)

        functions.addActions([action_search,action_learn])

        dics=menu_bar.addMenu('切换字典')

        action_IELTS=QAction('IELTS',self)
        action_IELTS.triggered.connect(lambda: self.switch('IELTS'))

        action_TOEFL=QAction('TOEFL',self)
        action_TOEFL.triggered.connect(lambda: self.switch('TOEFL'))

        dics.addActions([action_IELTS,action_TOEFL])
if __name__=='__main__':
    app=QApplication(sys.argv)
    window=MainWindow('test_user','IELTS')
    window.show()
    sys.exit(app.exec())
