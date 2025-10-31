#utils.py
'''注意：引用此文档可能会改变工作目录
    请谨慎引用
'''

from file_utils import load_data
from config import FILES
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将工作目录设置为脚本所在目录
os.chdir(current_dir)

print(f"现在工作目录是：{os.getcwd()}")

file_path=FILES['DICT']['TOEFL']

df = load_data(file_path,'TOEFL')
#如果使用其他文档，可能需要更改df的目录以及global_methods中的handle函数
