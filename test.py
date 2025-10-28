import numpy as np
import pandas as pd
import os
import random
from data_manager import *
from utils import df
from json_utils import JsonManager
from config import FILES

Df=Data(df)
def test_df():
    E=[]
    try:
        try:
            n=random.randint(0,len(df))
            Df.search_coordinate(n)
        except:
            raise 'search_coordinate出错'
        try:
            print(Df.search_word('n','first match'))
        except:
            raise 'search_word出错'
        try:
            Df.get_random_word()
        except:
            raise 'get_random_word出错'
        try:
            Df.get_details('all')
        except:
            raise 'get_drtails出错'
    except Exception as e:
        E.append(e)
    finally:
        if len(E)==0:
            return '正常运行'
        else:
            return f'出错如下：{E}'
        
def test_json_manager():
    # 使用临时文件进行测试
    test_file = FILES['SAVE']['test']
    
    # 清理可能存在的测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    
    try:
        # 创建管理器
        manager = JsonManager(test_file)
        
        # 测试创建账户
        result = manager.create_new_account("test_user", "test_password")
        print(f"创建新用户结果: {result}")  # 应该是 False（创建成功）
        
        # 测试重复创建
        result = manager.create_new_account("test_user", "test_password")
        print(f"重复创建用户结果: {result}")  # 应该是 True（用户已存在）
        
        # 测试记录单词
        manager.record_word("test_user", 123, 1)
        
        # 测试掌握单词
        manager.mastered_word_record("test_user", 123)
        manager.star_word_record("test_user", 123)

        #测试关注重点单词
        manager.foucus_word_update('test_user')
        
        print(manager.output('test_user','learned'))
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
            

if __name__=='__main__':
    test_json_manager()
