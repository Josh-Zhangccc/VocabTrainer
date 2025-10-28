#json_utils.py
'''提供JsonManager类去创建json文件以储存、调用用户信息'''
import json
import os
from datetime import datetime
from file_utils import test_form,open_fuc
from config import preferences

class JsonManager:
    """初始化储存用户信息的JSON文件，同时提供修改、更新、储存和删除的函数。
    是集中处理JSON文件的综合类
    """
    def __init__(self,file_path):
        self.file_path=file_path
        self.data=self.load_json()

    def load_json(self):
        if os.path.exists(self.file_path):
            return open_fuc(test_form(self.file_path),self.file_path)
        else:
            return self.create_default_json()

    def create_default_json(self):
        '''创建初始json文件的结构'''
        return{
            'users':{},
            'user_information':{},
            'version':1.0,
            'created_time': datetime.now().isoformat()[0:16],
            'last_update_time': datetime.now().isoformat()[0:16]
        }
    
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
        
    def create_new_account(self,user_id: str,user_key)-> bool:
        """创建一个新的用户，并自动更新用户信息
        如果已经存在该用户，则返回True
        需要while或其他循环来持续调用以保证用户体验的流畅性
        """
        if user_id not in self.data['users']:
            self.data['users'][user_id]={'name':f'{user_id}',
                                               'key':f'{user_key}',
                                               'created_time': datetime.now().isoformat()[0:16],
                                               'last_load_time': datetime.now().isoformat()[0:16]}
            self.data['user_information'][user_id]={'learned_words':{},
                                                    'mastered_words':[],
                                                    'star_words':[],
                                                    'high_focus_words':[],
                                                    'preferences':preferences
                                                    }
            return False
        else:
            return True
        
    def indiviualize(self,user_id:str,daily_word:int,frequency:int,review_mode:str,background:str) ->None:
        if (daily_word>0,
            frequency>0,
            review_mode in['L','M','H'],
            background in ['light','dark']):

            p=self.data['user_information'][user_id]['preferences']
            p['daily_words']=daily_word
            p['background']=background
            p['frequency']=frequency
            p['review_mode']=review_mode

    def record_word(self, user_id: str, wordrank: int, rank: int) -> None:
        """用途：记录已经学习过的单词,同时记录:学习的次数,
                                            第一次和最后一次学习的时间,
                                            以及自我评价的等级（0——5）"""
        if user_id not in self.data['users']:
            raise Exception(f'用户{user_id}不存在！')
        
        user_info = self.data['user_information'][user_id]
        if not isinstance(user_info['learned_words'], dict):
            user_info['learned_words'] = {}
        
        learned_words = user_info['learned_words']
        
        # 更清晰的写法：明确检查字典键
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

    def mastered_word_record(self,user_id:str,workrank:int) -> None:
        lis=self.data['user_information'][f'{user_id}']['mastered_words']
        if workrank not in lis:
            lis.append(workrank)

    def mastered_word_remove(self,user_id:str,workrank:int) -> None:
        lis=self.data['user_information'][f'{user_id}']['mastered_words']
        if workrank in lis:
            lis.remove(workrank)

    def star_word_record(self,user_id:str,workrank:int) -> None:
        lis=self.data['user_information'][f'{user_id}']['star_words']
        if workrank not in lis:
            lis.append(workrank)

    def star_word_remove(self,user_id:str,workrank:int) -> None:
        lis=self.data['user_information'][f'{user_id}']['star_words']
        if workrank in lis:
            lis.remove(workrank)

    def foucus_word_update(self,user_id:str) -> None:
        '''在preferences里提供三种关注度，low，middle，high。
        用途：根据不同的逻辑关注已学习但是需要复习的单词
        '''
        mode= self.data['user_information'][user_id]['preferences']['review_mode'] #str
        words=self.data['user_information'][user_id]['learned_words'] #dict
        foucus=self.data['user_information'][user_id]['high_focus_words'] #list
        foucus=[]
        print(mode,words,foucus)
        for wordrank,information in words.items(): #wordrank:int,inforamtion:dict
            rank=information['mastery_level']#list
            match mode:
                case 'L':
                    if rank[-1]<=2:
                        foucus.append(wordrank)
                case 'M':
                    if len(rank)>1:
                        if (rank[-1]+rank[-2])/2 <=3:
                            foucus.append(wordrank)
                    else:
                        if rank[-1]<=3:
                            foucus.append(wordrank)
                case 'H':
                    sum=0
                    for i in rank:
                        sum+=i
                    if sum/len(rank)<=3.5:
                        foucus.append(wordrank)
                case _:
                    pass

    def output(self,user_id:str,content:str) -> list:
        user_info=self.data['user_information'][user_id]
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
            case _:
                return []

class UserManager(JsonManager):
    def __init__(self,user_id:str,user_key:str,file_path):
        super().__init__(file_path)
        self.user_id=user_id
        self.user_key=user_key

    def loan(self):
        while self.user_id in self.data['users']:
            if self.user_key==self.data['users']['key']:
                return True
            else:
                return False


            