import pandas as pd
import json
import pickle
import gzip



def test_form(file_path:str)->str:
    '''用于检索文件类型'''
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print("✅ 用 JSON 读取成功！")
            return 'utf-8'
    except UnicodeDecodeError:
        print("❌ 不是 UTF-8 编码的文本文件，尝试二进制格式...")

        # 尝试用 pickle 读取
        try:
            with open(file_path, 'rb') as f:
                print("✅ 用 Pickle 读取成功！")
            return 'rb'
        except Exception as e:
            print(f"❌ 不是 Pickle 文件: {e}")

            try:
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    print("✅ 用 Gzip + JSON 读取成功！")
                return 'g'
            except Exception as e:
                print(f"❌ 不是 Gzip 文件: {e}")
                raise


def open_fuc(form,file_path):
    '''读取文件'''
    if form=='utf-8':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif form=='rb':
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    elif form=='g':
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            return json.load(f)
    else:
        print('='*50)
        print('FormError')
        raise ValueError("无法识别文件格式")
    

def load_data(file_path,form):
    '''加载文件并转换文件格式'''
    d=open_fuc(test_form(file_path),file_path)
    df_ori = pd.json_normalize(d)
    print(df_ori.iloc[0])
    match form:
        case 'IELTS':
            df=df_ori.iloc[:,[0,1,5,13,16,21,23]] 
            df.columns=['wordrank','word','sentences','synos','phrases','rels','trans'] 
        #case 'GRE':
         #   df=df_ori.iloc[:,[0,1,8,9,15,17,19]]#0wordRank ，1headWord  ，8trans ，9sentences，15syno，17.rels, 19phrases
          #  df.columns=['wordrank','word','trans','sentences','synos','rels','phrases']

        case 'TOEFL':
            df=df_ori.iloc[:,[0,1,5,8,13,16,19]]#0wordRank ，1headWord  5sentences,8synos，13phar,16rel,19trans
            df.columns=['wordrank','word','sentences','synos','phrases','rels','trans']

    df=df[['wordrank','word','sentences','synos','phrases','rels','trans']]
    df['firstletter']=df['word'].str[0]
    return df
