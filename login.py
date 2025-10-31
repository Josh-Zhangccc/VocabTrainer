import pandas as pd
from  data_manager import *
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                               QPushButton, QLabel, QVBoxLayout, 
                               QLineEdit,QWidget,QMessageBox,
                               QStatusBar)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from json_utils import JsonManager,AccountsManager,UserManager
from main import MainWindow
from utils import df
import time
AM=AccountsManager()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login_time=0
        self.setWindowTitle('登录')
        self.setGeometry(500,300,400,350)

        self.input_user_id=QLineEdit()
        self.input_user_id.setPlaceholderText('请输入您的用户名：')
        self.input_user_key=QLineEdit()
        self.input_user_key.setPlaceholderText('请输入您的密码：')
        self.input_user_key.setEchoMode(QLineEdit.Password)
        
        self.button_confirm=QPushButton('登录',self)
        self.button_register=QPushButton('还没有账号？注册一下',self)



        layout=QVBoxLayout()
        layout.addWidget(self.input_user_id)
        layout.addWidget(self.input_user_key)
        layout.addWidget(self.button_confirm)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

        self.button_confirm.clicked.connect(self.on_confirm_clicked)
        self.button_register.clicked.connect(self.on_register_cilcked)



    def judge_login(self):
        id = str(self.input_user_id.text()).strip()
        key= str(self.input_user_key.text()).strip()
        a=(id=='')
        b=(key=='')

        match (a,b):
            case (True,True):
                self.input_user_key.setPlaceholderText('密码不能为空')
                self.input_user_id.setPlaceholderText('用户名不能为空')
            case (True,False):
                self.input_user_id.setPlaceholderText('用户名不能为空')
            case (False,True):
                self.input_user_key.setPlaceholderText('密码不能为空')
            case (False,False):
                if AM.login(id,key):
                    print('成功登录')
                    return True
                else:
                    print('登录失败')
                    if not AM.check_user(id):
                        self.input_user_id.setPlaceholderText('用户名不存在')
                        self.input_user_id.clear()
                        self.input_user_key.setPlaceholderText('请输入您的密码：')
                        self.input_user_key.clear()
                        return False
                    else:
                        self.input_user_key.setPlaceholderText('密码错误')
                        self.input_user_key.clear()
                        return False
                    
    def open_main(self):
        self.main_window = MainWindow(df)
        self.main_window.show()
        self.close()

    def on_confirm_clicked(self):
        # 直接进行登录验证，不需要循环和递归
        res = self.judge_login()
        
        if res:
            self.open_main()
        else:
            self.login_time += 1
            print(f'尝试第 {self.login_time} 次')
            
            if self.login_time >= 3:
                self.input_user_id.setPlaceholderText('试错超过三次！禁止进入')
                self.input_user_id.setEnabled(False)  # 禁用输入框
                self.input_user_key.setEnabled(False)  # 禁用输入框
                self.button_confirm.setEnabled(False)  # 禁用登录按钮
                
                # 使用QTimer延迟关闭，避免阻塞UI
                from PySide6.QtCore import QTimer
                QTimer.singleShot(3000, self.close)
                    
        if self.login_time==3:
            self.input_user_id.setPlaceholderText('试错超过三次！禁止进入')
            time.sleep(3)
            self.close()

    def on_register_cilcked(self):
        self.register_window=RegisterWindow()
        self.register_window.show()
        self.close()

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('登录')
        self.setGeometry(500,300,400,350)

        self.input_user_id=QLineEdit()
        self.input_user_id.setPlaceholderText('请输入您的用户名：')

        self.input_user_key=QLineEdit()
        self.input_user_key.setPlaceholderText('请输入您的密码：')
        #self.input_user_key.setEchoMode(QLineEdit.Password)

        self.input_confirm_key=QLineEdit()
        self.input_confirm_key.setPlaceholderText('请确认您的密码：')
        #self.input_confirm_key.setEchoMode(QLineEdit.Password)

        self.button_register=QPushButton()
        self.button_register.setText('注册')

        layout=QVBoxLayout()

        layout.addWidget(self.input_user_id)
        layout.addWidget(self.input_user_key)
        layout.addWidget(self.input_confirm_key)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

        self.button_register.clicked.connect(self.on_register_clicked)
    

    def on_register_clicked(self):
        id = str(self.input_user_id.text()).strip()
        key= str(self.input_user_key.text()).strip()
        _key= str(self.input_confirm_key.text()).strip()

        a=(id=='')
        b=(key=='')
        c=(_key=='')
        identical=(key==_key)

        match (a,b,c):
            case (True,False,False):
                QMessageBox.information(self,'ATTENTION','请输入用户名')
            case (False,True,True) :
                QMessageBox.warning(self,'Warning',"请输入密码")                
            case (False,False,True):
                QMessageBox.information(self,'ATTENTION','请核验密码')  
            case (False,False,False):
                if identical==True:
                    if AM.create_new_account(id,key):
                        self.input_user_id.setPlaceholderText('用户名已存在！')
                        self.input_user_id.clear()
                    else:
                        self.button_register.setText('注册成功')
                        AM.save_json()
                        from PySide6.QtCore import QTimer
                        QTimer.singleShot(3000, self.close)
                        self.open_main()
                else:
                    self.input_confirm_key.clear()
                    self.input_user_key.clear()
                    QMessageBox.warning(self,'Warning','请确保两次密码输入一致！')
            case _:
                QMessageBox.information(self,'ATTENTION','请输入完整信息')


    def open_main(self):
        self.main_window = MainWindow(df)
        self.main_window.show()
        self.close()






if __name__=='__main__':
    app=QApplication(sys.argv)
    window=LoginWindow()
    window.show()
    sys.exit(app.exec())
