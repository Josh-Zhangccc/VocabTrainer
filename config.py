import os
from datetime import datetime
preferences={'daily_words':10,
            'background':'dark',
            'frequency':1,
            'review_mode':'M'
            }

current_dir = os.path.dirname(os.path.abspath(__file__))
FILES={'DICT':{'IELTS':os.path.join(current_dir,'data','IELTS_2.json')
               },
       'SAVE':{'test':os.path.join(current_dir,'data','test_file.json'),
               'accounts':os.path.join(current_dir,'data','accounts.json')
               }
       }
                                                    
glob_stru={
            'users':{},
            'version':2.0,
            'created_time':datetime.now().isoformat()[0:16]
        }
''' ['users'][user_id]={'name':f'{user_id}',
                        'key':f'{user_key}',
                        'learned_words':0
                                        }'''

user_stru={
            'learned_words':{},
            'mastered_words':[],
            'star_words':[],
            'high_focus_words':[],
            'preferences':preferences,
            'login_time':[datetime.now().isoformat()[0:16]]
        }