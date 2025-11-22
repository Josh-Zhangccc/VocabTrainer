from config import *
from .json_manager import JsonManager

class AccountsManager(JsonManager):
    '''AM=AccountsManager,无需设置jm
    管理accounts.json文件的类
    可以创建新用户，核验用户账号，修改用户信息和删除用户
    '''
    def __init__(self):
        super().__init__(FILES['SAVE']['accounts'],glob_stru)
        self.save_json()
        self.counts = self.data['counts']           #用户数
        self.dic_counts = self.data['dic_counts']    #个人字典数
           
    def create_new_account(self,user_id: str,user_key)-> bool:
        """创建一个新的用户，并自动更新用户信息
        如果已经存在该用户，则返回True
        需要while或其他循环来持续调用以保证用户体验的流畅性
        """
        if user_id not in self.data['users']:
            self.data['users'][user_id]={'name':f'{user_id}',
                                          'key':f'{user_key}',
                                          'learned_words':0
                                        }
            self.data['counts']+=1
            self.counts = self.data['counts']
            return False
        else:
            return True
                
    def learn_one_new_word(self,user_id:str) -> None:
        if user_id in self.data['users']:
            self.data['users'][user_id]['learned_words']+=1
        
    def del_account(self,user_id:str,user_key:str) -> bool:
        if self.login(user_id,user_key):
                del(self.data['users'][user_id])
                self.data['counts'] -= 1
                self.counts = self.data['counts']
                return False
        else:
            return True

    def check_user(self,user_id):
        '''检索用户是否存在，符合返回True,否则返回False
        '''
        if user_id in self.data['users']:
            return True
        else:
            return False
        
    def login(self,user_id,user_key):
        '''输入用户id和密码，如果符合的话返回True,否则返回False
        '''
        if self.check_user(user_id):
            key=self.data['users'][user_id]['key'] # str
            if not isinstance(user_key,str):
                user_key=str(user_key)
            if user_key==key:
                return True
            else:
                return False
        else:
            return False
       
    def add_dic(self):
        self.data['dic_counts'] += 1
        self.counts = self.data['dic_counts']

    def del_dic(self):
        self.data['dic_counts'] -= 1
        self.counts = self.data['dic_counts']
