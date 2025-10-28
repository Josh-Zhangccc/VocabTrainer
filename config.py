import os

preferences={'daily_words':10,
            'background':'dark',
            'frequency':1,
            'review_mode':'M'
            }

current_dir = os.path.dirname(os.path.abspath(__file__))

FILES={'DICT':{'IELTS':os.path.join(current_dir,'data','IELTS_2.json')
               },
       'SAVE':{'test':os.path.join(current_dir,'data','teat_file.json'),
               'work':os.path.join(current_dir,'data','\work_data.json')
               }
       }
                                                    
