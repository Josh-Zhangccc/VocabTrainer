import numpy as np
import pandas as pd
import os
import random
from data_manager import *
#from utils import df
from json_utils import *
from config import FILES
'''
Df=Data(df)
def test_df():
    E=[]
    try:
        try:
            n=random.randint(0,len(df))
            print(Df.search_coordinate(1))
        except:
            raise 'search_coordinate出错'
        try:
            print(Df.search_word('n','first match'))
        except:
            raise 'search_word出错'
        try:
            print(Df.get_random_word())
        except:
            raise 'get_random_word出错'
        try:
            print(Df.get_details('all'))
        except:
            raise 'get_drtails出错'
    except Exception as e:
        E.append(e)
    finally:
        if len(E)==0:
            return '正常运行'
        else:
            return f'出错如下：{E}'
        '''
def test_json_manager():
    AM=AccountsManager()

    # 使用临时文件进行测试
    test_file = FILES['SAVE']['test']
    
    # 清理可能存在的测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    if AM.check_user('test_user'):
        try:
            # 创建管理器
            manager = UserManager('test_user','TOEFL')
            
            manager.indiviualize(20,2,'L','dark')
            
            # 测试记录单词
            manager.record_word(123,1)
            
            # 测试掌握单词
            manager.mastered_word_record(123)
            manager.star_word_record(123)

            #测试关注重点单词
            manager.focus_word_update()
            
            print(manager.output('learned'))
            # 测试保存
            save_result = manager.save_json()
            print(f"保存结果: {save_result}")
            
            print("所有测试通过！")
            
        except Exception as e:
            print(f"测试失败: {e}")
        '''finally:
            # 清理测试文件
            if os.path.exists(test_file):
                os.remove(test_file)'''
    else:
        print('用户不存在')
        AM.create_new_account('test_user','123456')
        AM.save_json()
        UserManager('test_user')
            

if __name__=='__main__':
 #   print(test_df())
 #   print(df.head())
 #  test_json_manager()
    UM=UserManager('test_user','IELTS')