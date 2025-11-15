import os
from datetime import datetime
preferences={'daily_words':10,
            'background':'dark',
            'frequency':1,
            'review_mode':'M'
            }

current_dir = os.path.dirname(os.path.abspath(__file__))
FILES={'DICT':{'IELTS':os.path.join(current_dir,'data','dict','IELTS.json'),
               'GRE':os.path.join(current_dir,'data','dict','GRE.json'),
               'TOEFL':os.path.join(current_dir,'data','dict','TOEFL.json')
               },
       'SAVE':{'test':os.path.join(current_dir,'data','test_file.json'),
               'accounts':os.path.join(current_dir,'data','accounts.json')
               }
       }
                                                    
glob_stru={
            'users':{},                                         #各用户信息
            'version':2.0,                                      #版本
            'count':0,                                          #总用户数
            'dic_count':0,
            'created_time':datetime.now().isoformat()[0:16]     #创建时间
        }
''' ['users'][user_id]={'name':f'{user_id}',
                        'key':f'{user_key}',
                        'learned_words':0
                                        }'''

user_stru={ 'dic':{},                                           #已开始学习的字典
            'preferences':preferences,                          #个性化参数
            'login_time':[datetime.now().isoformat()[0:16]],    #登录时间
            'dic_info':[]                                       #个性化单词列表，这里仅提供一个编号
        }


'''            'learned_words':{},
            'mastered_words':[],
            'star_words':[],
            'high_focus_words':[],
'''
DIC=['IELTS','TOEFL']


word_stru={
              "wordRank": "",
              "headWord": "",
              "content": {
              "word": {
                  "wordHead": "",
                  "wordId": "",
                  "content": {
                  "sentence": {
                      "sentences": [],
                      "desc": ""
                  },
                  "usphone": "",
                  "antos": {
                      "anto": [],
                      "desc": "反义"
                  },
                  "ukspeech": "",
                  "star": 0,
                  "usspeech": "",
                  "syno": {
                      "synos": [],
                      "desc": "同近"
                  },
                  "ukphone": "",
                  "phrase": {
                      "phrases": [],
                      "desc": "短语"
                  },
                  "speech": "",
                  "remMethod": {
                      "val": "",
                      "desc": ""
                  },
                  "relWord": {
                      "rels": [],
                      "desc": "同根"
                  },
                  "trans": []
                }
              }
              },
              "bookId": ""
        }