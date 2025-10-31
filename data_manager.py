#data_manager.py
'''提供Data类'''
import pandas as pd
import random

class Data:
    '''该类提供对于已处理的字典的截取，检索和输出
    除特定条件外，输出结果均为Series
    本类中提供变量：ClassName=Data(df) -> ClassName.series
    使输出切片时多者符合同一性
    '''
    def __init__(self,df):
        self.df=df
        self.series=pd.Series()
        self.content={'workrank':0,
                  'word':1,
                  'sentences':2,
                  'synos':3,
                  'phrases':4,
                  'rels':5,
                  'trans':6,
                  'firstletter':7
                  }
        self.dic = {'1': 'a','2': 'b','3': 'c',
                    '4': 'd','5': 'e','6': 'f',
                    '7': 'g','8': 'h','9': 'i',
                    '10': 'j','11': 'k','12': 'l',
                    '13': 'm','14': 'n','15': 'o',
                    '16': 'p','17': 'q','18': 'r',
                    '19': 's','20': 't','21': 'u',
                    '22': 'v','23': 'w','24': 'x',
                    '25': 'y','26': 'z'
                    }
        self.dic_reverse= {value: key for key, value in self.dic.items()}
    
    def __str__(self):
        return self.df
    
    def __len__(self):
        return len(self.df)
    
    def transform(self,column_name):
        '''通过column_name来得到对应的表头'''
        return self.content.get(f'{column_name}','WrongName')
    
        #通过self引入其他函数
    
    def search_coordinate(self,index,column=None):
        '''通过坐标去检索单词/词组，提供index=‘all’的方法输出所有符合的单词,column在无输入的情况下输出整行.

        index,column为具体值，返回list.
        index为具体值，column为None，返回Series.
        index='all',不推荐.
        '''
        #转换index的格式
        if isinstance(index, (int, str)) and str(index).isdigit():
            index=int(index)
        elif index=='all':
            pass
        else:
            raise ValueError("index must be 'all' or a number")
        
        #具体判断
        if column==None:
            if index=='all':
                return self.df
            else:
                return self.df.iloc[index,:]
        else:
            col=self.transform(column)
            if index=='all':
                return self.df.iloc[:,col]
            else:
                return self.df.iloc[index,col]

    def first_letter_divide(self,fl) -> pd.DataFrame:
        '''支持用数字和具体大小写单词去获取由首字母分割的Dataframe'''
        if isinstance(fl,(str,int)):
            if fl in range(1,27):
                fl=self.dic.get(str(fl))
            else:
                fl=fl.lower()
                if self.dic_reverse.get(fl,False):
                    pass
                else:
                    raise ValueError
            df_fl=self.df.query('firstletter == @fl')
            return df_fl
        else:
            raise TypeError
        
    def search_word(self, word, method='fuzzy'):
        '''通过具体的字符串来获取单词的位置。如果模糊搜索单项，则 返回Series。
            'method'提供'accurate'，'first match'，'fuzzy'，'first fuzzy'四种'''
        
        try:
            match method:
                case 'accurate':
                    df_search = self.df.query("word == @word")
                    if len(df_search) == 0:
                        return None
                    self.series=df_search.iloc[0]
                    return df_search.iloc[0]
                    
                case 'first match':
                    df_search = self.df[self.df['word'].str.contains(word)]
                    if len(df_search) == 0:
                        return None
                    self.series=df_search.iloc[0]
                    return df_search.iloc[0]
                    
                case 'fuzzy':
                    df_search = self.df[self.df['word'].str.contains(word)]
                    if len(df_search) == 0:  # 添加空结果检查
                        return None
                    elif len(df_search) == 1:
                        self.series=df_search.iloc[0]
                        return df_search.iloc[0]
                    else:
                        return df_search
                        
                case 'first fuzzy':
                    # 先根据首字母缩小搜索范围
                    df_first_letter = self.first_letter_divide(word[0])
                    df_search = df_first_letter[df_first_letter['word'].str.contains(word)]  # 修正：在缩小范围后的数据中搜索
                    if len(df_search) == 0:  # 添加空结果检查
                        return None
                    elif len(df_search) == 1:
                        self.series=df_search.iloc[0]
                        return df_search.iloc[0]
                    else:
                        return df_search
                        
                case _:
                    raise ValueError(f"未知的搜索方法: {method}")
                    
        except Exception as e:
            # 如果有 file_path 属性就使用，否则用通用提示
            print(f"错误: {e}, 未检索到'{word}'")
            return None  # 统一返回 None 而不是 False
    
        
    @staticmethod
    def divide(res:pd.Series,column:str):
        '''可单独使用，提供对于数据库的具体分割方法
        总是返回："xx---xx"*n
        ATTENTION：请提供相应的res(type:list)'''

        output = ""
        if column == 'sentences':
            parts = []
            if res is None:
                return ""
            for i in res:
                parts.append(f"{i.get('sContent','')}---{i.get('sCn','')}")
            output = "\n".join(parts)

        elif column == 'synos':
            parts = []
            if res is None:
                return ""
            for i in res:
                parts.append(f"{i.get('pos','')}---{i.get('tran','')}")
                for j in i.get('hwds', []):
                    parts.append(f"similar---{j.get('w','')}")
            output = "\n".join(parts)

        elif column == 'phrases':
            parts = []
            if res is None:
                return ""
            for i in res:
                parts.append(f"{i.get('pContent','')}---{i.get('pCn','')}")
            output = "\n".join(parts)

        elif column == 'rels':
            parts = []
            if res is None:
                return ""
            for i in res:
                parts.append(f"{i.get('pos','')}")
                for j in i.get('words', []):
                    parts.append(f"{j.get('hwd','')}---{j.get('tran','')}")
            output = "\n".join(parts)

        elif column =='trans':
            parts=[]
            if res is None:
                return ''
            for i in res:
                parts.append(f"{i.get('pos','')}---{i.get('tranCn','')}")
                output = "\n".join(parts)
        else:
            output = str(res)

        return output 

    @staticmethod
    def handle(Series:pd.Series,column:str)->list:
        '''单独使用，获取具体Series的某一数据，返回list
        ATTENTION：请提供具体的Series！'''
        try:
            res=Series[f'{column}']
            if res is None or (isinstance(res, float) and pd.isna(res)):
                return ""
            else:
                return Data.divide(res,column)
        except Exception as e:
            raise e
    
    def re_init(self)->None:
        '''重新初始化self.series这个变量，以保证程序正常运行
        '''
        self.series=pd.Series()
        
    def get_random_word(self,get_word:bool=False):
        '''随机获取一个单词的Series;
        当get_word=True时返回Series的单词
        '''
        index=random.randint(0,len(self.df)-1)
        self.series=self.search_coordinate(index)
        if not get_word:
            return self.series
        else:
            return self.series['word']
        
    def get_rw_besides(self,lis:list,get_word=False) ->pd.Series:
        '''输入一个每项是数字的列表，返回在self.df中除了该列表外的随机一个单词的Series'''
        def fun(lis):
                index=random.randint(0,len(self.df)-1)
                if index in lis:
                    fun()
                return index
        index=fun(lis)
        self.series=self.search_coordinate(index)
        if not get_word:
            return self.series
        else:
            return self.series['word']
    
    def get_details(self,content)->str:
        '''在handle的基础上增加了‘all’的输出'''
        if content=='all':
            output=''
            for i in['sentences','synos','phrases','rels','trans']:
                output+=f'\n\n{i}:'+f'{Data.handle(self.series,i)}'
            return output
        else:
            return Data.handle(self.series,content)
        
    def judge_self_series(self)->bool:
        if self.series.empty:
            return True
        else:
            return False
     


