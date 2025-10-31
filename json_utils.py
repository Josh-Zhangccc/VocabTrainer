#json_utils.py
'''提供JsonManager类去创建json文件以储存、调用用户信息
注意！所有的函数都没有自动保存的功能，轻调用save_json()手动设置保存时机'''
import json
import os
from datetime import datetime
from file_utils import test_form,open_fuc
from config import *
from data_manager import Data

class JsonManager:
    """初始化储存用户信息的JSON文件。
    jm=JsonManager(file_path,stru)
    自动创建一个json结构的文件/打开该路径的json文件
    save()函数提供保存功能
    """
    def __init__(self,file_path,stru):
        self.file_path=file_path
        self.stru=stru
        self.data=self.load_json()
        
    def load_json(self):
        if os.path.exists(self.file_path):
            return open_fuc(test_form(self.file_path),self.file_path)
        else:
            return self.create_json()

    def create_json(self):
        '''创建初始json文件的结构'''
        return self.stru
    
    def save_json(self) -> bool:
        """保存数据到JSON文件
        用途：将内存中的数据持久化到硬盘
        返回：成功True，失败False
        """
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False
        
class AccountsManager(JsonManager):
    '''AM=AccountsManager,无需设置jm
    管理accounts.json文件的类
    可以创建新用户，核验用户账号，修改用户信息和删除用户
    '''
    def __init__(self):
        super().__init__(FILES['SAVE']['accounts'],glob_stru)
        self.save_json()
           
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
            return False
        else:
            return True
        
    def learn_one_new_word(self,user_id:str) -> None:
        if user_id in self.data['users']:
            self.data['users'][user_id]['learned_words']+=1

        
    def del_account(self,user_id:str,user_key:str) -> bool:
        if user_id in self.data['users']:
            if user_key==self.data['users'][user_id]['key']:
                del(self.data['users'][user_id])
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
       
class UserManager(JsonManager):
    '''UM=UserManager(user_id)
    管理单个用户具体信息的方法
    提供个性化服务，已学、掌握、标记单词的添加和删除方法，重点单词的确定逻辑和
    输出用户具体信息的方法
    '''
    def __init__(self,user_id):
        user_data_path = os.path.join(current_dir, 'data',f'{user_id}.json')
        super().__init__(user_data_path,user_stru)
        self.user_id=user_id
        self.save_json()
        
    def indiviualize(self,daily_word:int,frequency:int,review_mode:str,background:str) ->None:
        if (daily_word>0,
            frequency>0,
            review_mode in['L','M','H'],
            background in ['light','dark']):

            p=self.data['preferences']
            p['daily_words']=daily_word
            p['background']=background
            p['frequency']=frequency
            p['review_mode']=review_mode

    def choose_dic(self):
        pass

    def record_word(self, wordrank: int, rank: int) -> None:
        """用途：记录已经学习过的单词,同时记录:学习的次数,
                                            第一次和最后一次学习的时间,
                                            以及自我评价的等级（0——5）"""
        
        if not isinstance(self.data['learned_words'], dict):
            self.data['learned_words'] = {}
        
        learned_words = self.data['learned_words']
        
        if wordrank not in learned_words.keys():
            learned_words[wordrank] = {
                'time': [datetime.now().isoformat()[0:16]],
                'times': 1,
                'mastery_level': [rank]
            }
        else:
            learned_words[wordrank]['time'].append(datetime.now().isoformat()[0:16])
            learned_words[wordrank]['times'] += 1
            learned_words[wordrank]['mastery_level'].append(rank)

    def mastered_word_record(self,workrank:int) -> None:
        lis=self.data['mastered_words']
        if workrank not in lis:
            lis.append(workrank)

    def mastered_word_remove(self,workrank:int) -> None:
        lis=self.data['mastered_words']
        if workrank in lis:
            lis.remove(workrank)

    def star_word_record(self,workrank:int) -> None:
        lis=self.data['star_words']
        if workrank not in lis:
            lis.append(workrank)

    def star_word_remove(self,workrank:int) -> None:
        lis=self.data['star_words']
        if workrank in lis:
            lis.remove(workrank)

    def focus_word_update(self) -> None:
        '''在preferences里提供三种关注度，low，middle，high。
        用途：根据不同的逻辑关注已学习但是需要复习的单词'''
        
        mode= self.data['preferences']['review_mode'] #str
        words=self.data['learned_words'] #dict
        focus=self.data['high_focus_words'] #list
        focus=[]
        print(mode,words,focus)
        for wordrank,information in words.items(): #wordrank:int,inforamtion:dict
            rank=information['mastery_level']#list
            match mode:
                case 'L':
                    if rank[-1]<=2:
                        focus.append(wordrank)
                case 'M':
                    if len(rank)>1:
                        if (rank[-1]+rank[-2])/2 <=3:
                            focus.append(wordrank)
                    else:
                        if rank[-1]<=3:
                            focus.append(wordrank)
                case 'H':
                    sum=0
                    for i in rank:
                        sum+=i
                    if sum/len(rank)<=3.5:
                        focus.append(wordrank)
                case _:
                    pass
    
    def time_record(self):
        self.data['login_time'].append(datetime.now().isoformat()[0:16])

    def output(self,content:str) -> list:
        '''content:'learned','mastered','star','focus'
        返回用户对应的数据，形式为列表
        '''
        user_info=self.data
        match content:
            case 'learned':
                words=[]
                for workrank,value in user_info['learned_words'].items():
                    words.append(workrank)
                return words
            case 'mastered':
                return user_info['mastered_words']
            case 'star':
                return user_info['star_words']
            case 'focus':
                return user_info['high_focus_words']
            case _:
                return []

    def learn(self) -> str:
        words=self.output('learned') #list


