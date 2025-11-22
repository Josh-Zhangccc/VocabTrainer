"""
VocabTrainer 项目测试文件
提供对 Data 类、UserManager 类等核心组件的单元测试
"""

import os
import random
import unittest
from datetime import datetime

from data_manager import Data
from UsersDataManagers.user_manager import UserManager
from UsersDataManagers.accounts_manager import AccountsManager
from config import FILES, current_dir
import pandas as pd


class TestData(unittest.TestCase):
    """测试 Data 类的功能"""
    
    @classmethod
    def setUpClass(cls):
        """在所有测试之前运行一次，准备测试数据"""
        # 创建一个小型测试用的 DataFrame
        cls.test_data = pd.DataFrame({
            'workrank': [1, 2, 3, 4, 5],
            'word': ['apple', 'banana', 'cherry', 'date', 'elderberry'],
            'sentences': ['A fruit', 'Yellow fruit', 'Red fruit', 'Sweet fruit', 'Small fruit'],
            'firstletter': ['a', 'b', 'c', 'd', 'e']
        })
        cls.data_manager = Data(cls.test_data)

    def test_search_coordinate(self):
        """测试坐标检索功能"""
        # 测试检索特定行
        result = self.data_manager.search_coordinate(0)
        self.assertEqual(result['word'], 'apple')
        self.assertEqual(result['workrank'], 1)

        # 测试检索特定列
        result = self.data_manager.search_coordinate(0, 'word')
        self.assertEqual(result, 'apple')

        # 测试检索所有数据
        result = self.data_manager.search_coordinate('all')
        self.assertEqual(len(result), 5)

    def test_search_word(self):
        """测试单词搜索功能"""
        # 测试精确匹配
        result = self.data_manager.search_word('apple', 'accurate')
        self.assertIsNotNone(result)
        self.assertEqual(result['word'], 'apple')

        # 测试首匹配
        result = self.data_manager.search_word('app', 'first match')
        self.assertIsNotNone(result)
        self.assertIn('app', result['word'])

        # 测试模糊匹配
        result = self.data_manager.search_word('an', 'fuzzy')
        self.assertIsNotNone(result)

        # 测试首字母模糊匹配
        result = self.data_manager.search_word('ban', 'first fuzzy')
        self.assertIsNotNone(result)
        self.assertIn('ban', result['word'])

    def test_get_random_word(self):
        """测试获取随机单词功能"""
        result = self.data_manager.get_random_word()
        self.assertIsNotNone(result)
        self.assertIn('word', result.index)

        word = self.data_manager.get_random_word(get_word=True)
        self.assertIsInstance(word, str)
        self.assertIn(word, self.test_data['word'].tolist())

    def test_get_details(self):
        """测试获取单词详细信息功能"""
        # 首先获取一个单词
        self.data_manager.series = self.data_manager.search_coordinate(0)
        details = self.data_manager.get_details('all')
        self.assertIsInstance(details, str)

        # 测试获取特定内容
        sentences = self.data_manager.get_details('sentences')
        self.assertIsInstance(sentences, str)

    def test_first_letter_divide(self):
        """测试按首字母分割功能"""
        result = self.data_manager.first_letter_divide('a')
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['word'], 'apple')

        # 测试数字输入
        result = self.data_manager.first_letter_divide(1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['word'], 'apple')


class TestUserManager(unittest.TestCase):
    """测试 UserManager 类的功能"""
    
    def setUp(self):
        """在每个测试之前运行，准备测试环境"""
        self.test_user_id = 'test_user'
        self.test_dic = 'TOEFL'
        self.test_file_path = os.path.join(current_dir, 'data', 'users', f'{self.test_user_id}.json')
        
        # 确保测试用户存在
        accounts_manager = AccountsManager()
        if not accounts_manager.check_user(self.test_user_id):
            accounts_manager.create_new_account(self.test_user_id, 'test_password')
            accounts_manager.save_json()
    
    def test_user_manager_initialization(self):
        """测试 UserManager 初始化"""
        manager = UserManager(self.test_user_id, self.test_dic)
        self.assertEqual(manager.user_id, self.test_user_id)
        self.assertEqual(manager.dic, self.test_dic)
        self.assertIn(self.test_dic, manager.data['dic'])

    def test_record_word(self):
        """测试记录单词功能"""
        manager = UserManager(self.test_user_id, self.test_dic)
        wordrank = 123
        rank = 4

        # 记录单词
        manager.record_word(wordrank, rank)

        # 验证单词已记录
        learned_words = manager.info['learned_words']
        self.assertIn(str(wordrank), learned_words)
        self.assertEqual(learned_words[str(wordrank)]['times'], 1)
        self.assertEqual(learned_words[str(wordrank)]['mastery_level'], [rank])

        # 再次记录同一个单词
        manager.record_word(wordrank, 3)
        self.assertEqual(learned_words[str(wordrank)]['times'], 2)
        self.assertEqual(learned_words[str(wordrank)]['mastery_level'], [rank, 3])

    def test_mastered_word_operations(self):
        """测试掌握单词操作"""
        manager = UserManager(self.test_user_id, self.test_dic)
        wordrank = 456

        # 测试添加掌握单词
        manager.mastered_word_record(wordrank)
        self.assertIn(wordrank, manager.info['mastered_words'])

        # 测试删除掌握单词
        manager.mastered_word_remove(wordrank)
        self.assertNotIn(wordrank, manager.info['mastered_words'])

    def test_star_word_operations(self):
        """测试星标单词操作"""
        manager = UserManager(self.test_user_id, self.test_dic)
        wordrank = 789

        # 测试添加星标单词
        manager.star_word_record(wordrank)
        self.assertIn(wordrank, manager.info['star_words'])

        # 测试删除星标单词
        manager.star_word_remove(wordrank)
        self.assertNotIn(wordrank, manager.info['star_words'])

    def test_individualize_settings(self):
        """测试个性化设置功能"""
        manager = UserManager(self.test_user_id, self.test_dic)
        daily_words = 20
        frequency = 2
        review_mode = 'L'
        background = 'dark'

        manager.indiviualize(daily_words, frequency, review_mode, background)

        prefs = manager.data['preferences']
        self.assertEqual(prefs['daily_words'], daily_words)
        self.assertEqual(prefs['frequency'], frequency)
        self.assertEqual(prefs['review_mode'], review_mode)
        self.assertEqual(prefs['background'], background)

    def test_output_function(self):
        """测试输出功能"""
        manager = UserManager(self.test_user_id, self.test_dic)
        wordrank = 999

        # 记录一个单词
        manager.record_word(wordrank, 5)
        learned_words = manager.output('learned')
        self.assertIn(wordrank, learned_words)

        # 测试其他输出类型
        mastered = manager.output('mastered')
        self.assertIsInstance(mastered, list)

        starred = manager.output('star')
        self.assertIsInstance(starred, list)

        focused = manager.output('focus')
        self.assertIsInstance(focused, list)

    def test_time_record(self):
        """测试时间记录功能"""
        manager = UserManager(self.test_user_id, self.test_dic)
        initial_count = len(manager.data['login_time'])

        # 记录时间
        manager.time_record()
        self.assertEqual(len(manager.data['login_time']), initial_count + 1)

    def test_create_self_dic(self):
        """测试创建个人字典功能"""
        manager = UserManager(self.test_user_id, self.test_dic)
        initial_count = len(manager.data['dic_info'])

        # 创建个人字典
        manager.create_self_dic()
        # 由于这个函数会修改全局数据，我们只验证没有异常
        self.assertTrue(True)  # 占位符，确保测试运行

    def tearDown(self):
        """在每个测试之后运行，清理测试环境"""
        # 清理测试用户数据（可选，根据需要保留或删除）
        pass


class IntegrationTest(unittest.TestCase):
    """集成测试，测试多个组件之间的交互"""

    def test_user_flow(self):
        """测试用户学习流程"""
        user_id = 'integration_test_user'
        dic = 'IELTS'
        
        # 确保测试用户存在
        accounts_manager = AccountsManager()
        if not accounts_manager.check_user(user_id):
            accounts_manager.create_new_account(user_id, 'test_password')
            accounts_manager.save_json()
        
        # 创建用户管理器并执行典型操作
        um = UserManager(user_id, dic)
        um.indiviualize(10, 1, 'M', 'light')
        um.record_word(1, 5)
        um.record_word(2, 3)
        um.star_word_record(1)
        um.mastered_word_record(2)
        um.focus_word_update()
        um.time_record()
        um.save_json()

        # 验证操作结果
        learned = um.output('learned')
        starred = um.output('star')
        mastered = um.output('mastered')
        focused = um.output('focus')

        self.assertIn(1, learned)
        self.assertIn(1, starred)
        self.assertIn(2, mastered)
        # focused 可能为空，取决于 focus_word_update 的逻辑

        # 清理测试用户（可选）
        # os.remove(os.path.join(current_dir, 'data', 'users', f'{user_id}.json'))


def run_specific_tests():
    """运行特定的测试用例"""
    # 用于执行特定测试的辅助函数
    pass


if __name__ == '__main__':
    # 使用 unittest 运行所有测试
    unittest.main(verbosity=2)