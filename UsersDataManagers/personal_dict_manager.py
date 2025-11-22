import os
import config
from .json_manager import JsonManager


class PersonalDictManager(JsonManager):
    '''功能：创建个人词典
    添加/删除单词及其信息
    检索单词是否存在'''
    def __init__(self,user_id,num):
        self.num = num
        file_path= os.path.join(config.current_dir,'data','users',f'{user_id}',f'{user_id}-{num}.json') 

        if  not os.path.exists(file_path):
            JMaccounts = JsonManager(os.path.join(config.current_dir,'data','accounts.json'))
            JMaccounts.data['dic_counts'] +=1
            JMaccounts.save_json()
            JMuser = JsonManager(os.path.join(config.current_dir,'data','users',f'{user_id}',f'{user_id}.json'))
            JMuser.data['dic_info'].append(num)
            JMuser.save_json()

        super().__init__(file_path,[])#初始化的data结构为[]
        self.count=len(self.data)

    def check(self,word:str) -> bool:
        '''在个性化字典里进行检索，如果已存在该单词或与其相关的单词重复，则返回False
            存在：False
            不存在：True
            O(n^2)
        '''
        res=True #True代表没有任何的重复
        for i in self.data:
            if word !=i["headWord"]:

                try:
                    if any(word == j["words"][0]["hwd"] for j in i["content"]["word"]["content"]["relWord"]["rels"]):
                        res=False

                except KeyError:
                    continue

                finally:
                    print('检索完成！')

            else:
                res=False

            return res
    
    def add(self,word:str):
        '''生成一个单词的全部结构,同时自动修正单词的编码并清空有关内容
            但是不提供任何的检索功能，需要额外配合check函数进行判断
            原因：如果内嵌，则check在后续的各个函数中会被重复调用，消耗算力
            O(1)'''
        self.count+=1       #总单词数改变        
        wordrank=self.count
        added_word=config.word_stru
        added_word["wordRank"]=wordrank
        added_word["headWord"]=word
        added_word["content"]["word"]["wordHead"] = word
        added_word["bookId"]=self.num
        self.data.append(added_word)

    def delete(self,word:str):
        '''查找有关单词，直接删除全部信息
        '''
        for i in self.data:
            if i["headWord"] == word:
                self.data.remove(i)
                self.count-=1   #总单词数改变

    def update(self):
        for word,to_change_index in (range(len(self.data)),self.data):
            word["wordRank"] = to_change_index
