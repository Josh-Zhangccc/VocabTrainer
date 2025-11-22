import os
from datetime import datetime
from config import *
from .json_manager import JsonManager
from .accounts_manager import AccountsManager

class UserManager(JsonManager):
    '''
    管理单个用户具体信息的方法
    提供个性化服务，已学、掌握、标记单词的添加和删除方法，重点单词的确定逻辑和
    输出用户具体信息的方法
    Args:
        user_id: 用户名
        dic: 当前使用的字典

    Examples:
        >>> UM = UserManager(test_user,"IELTS")
        >>> UM.record_word(1,4)
        >>> UM.time_record()
        >>> UM.save_json()

    '''
    def __init__(self,user_id:str,dic:str="IELTS"):
        user_folder_path = os.path.join(current_dir, 'data','users',f'{user_id}')
        os.makedirs(user_folder_path,exist_ok=True)
        user_data_path = os.path.join(user_folder_path,f'{user_id}.json')
        self.dic=dic
        super().__init__(user_data_path,user_stru)
        if dic not in self.data['dic']:
            self.data['dic'][f'{self.dic}']={
                                            'learned_words':{},
                                            'mastered_words':[],
                                            'star_words':[],
                                            'high_focus_words':[]
                                            }
        self.info=self.data['dic'][self.dic]
        self.user_id=user_id
        self.save_json()

    def clear(self):
        '''清楚用户的全部数据'''
        self.data['dic'][self.dic]={
                                    'learned_words':{},
                                    'mastered_words':[],
                                    'star_words':[],
                                    'high_focus_words':[]
                                    }
        
    def indiviualize(self,daily_word:int,
                     frequency:int,
                     review_mode:str,
                     background:str) ->None:
        """调整用户的个性化设置
            Args:
                daily_word: 每天学习的单词数
                frequency: 单词重复出现的频率
                review_mode: HML三种模式，复习的难度
                background: 界面的颜色
        """
        if (daily_word>0,
            frequency>0,
            review_mode in['L','M','H'],
            background in ['light','dark']):

            p=self.data['preferences']
            p['daily_words']=daily_word
            p['background']=background
            p['frequency']=frequency
            p['review_mode']=review_mode
            print(self.data['preferences'])

    def dic_info(self):
        '''返回当前正在学习的字典'''
        return self.dic #str
    
    def record_word(self, wordrank: int, rank: int) -> None:
        """用途：记录已经学习过的单词,同时记录:学习的次数,第一次和最后一次学习的时间,以及自我评价的等级（0——5）
            Args:
                workrank: 单词的序号
                rank: 自我评价等级"""
        
        if not isinstance(self.info['learned_words'], dict):
            self.info['learned_words'] = {}
        
        learned_words = self.info['learned_words']
        wordrank=str(wordrank)
        if wordrank not in learned_words.keys():
            learned_words[f'{wordrank}'] = {
                'time': [datetime.now().isoformat()[0:16]],
                'times': 1,
                'mastery_level': [rank]
            }
        else:
            learned_words[wordrank]['time'].append(datetime.now().isoformat()[0:16])
            learned_words[wordrank]['times'] += 1
            learned_words[wordrank]['mastery_level'].append(rank)

    def mastered_word_record(self,workrank:int) -> None:
        """记录已经完全掌握的单词"""
        lis=self.info['mastered_words']
        if workrank not in lis:
            lis.append(workrank)

    def mastered_word_remove(self,workrank:int) -> None:
        """删除自认为完全掌握的单词"""
        lis=self.info['mastered_words']
        if workrank in lis:
            lis.remove(workrank)

    def star_word_record(self,workrank:int) -> None:
        """标记重点单词"""
        lis=self.info['star_words']
        if workrank not in lis:
            lis.append(workrank)

    def star_word_remove(self,workrank:int) -> None:
        """删除重点单词"""
        lis=self.info['star_words']
        if workrank in lis:
            lis.remove(workrank)

    def focus_word_update(self) -> None:
        '''根据不同的逻辑关注已学习但是需要复习的单词'''
        
        mode= self.data['preferences']['review_mode'] #str
        words=self.info['learned_words'] #dict
        focus=[]
        print(mode,words,focus)
        for wordrank,information in words.items(): #wordrank:str,inforamtion:dict
            wordrank=int(wordrank)
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
        self.info['high_focus_words'].clear()
        self.info['high_focus_words']=focus
        print(focus)
    
    def time_record(self):
        """记录登录时间"""
        self.data['login_time'].append(datetime.now().isoformat()[0:16])

    def output(self,content:str) -> list:
        '''
        返回用户对应的数据
        Args:
            content: 'learned','mastered','star','focus'
        '''
        user_info=self.info
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
            
    def create_self_dic(self):
        pass