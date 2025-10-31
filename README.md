![Python](https://img.shields.io/badge/Python-3.10%2B-blue)![License](https://img.shields.io/badge/License-MIT-green)
# 我的第一个个人小项目（半成品）：VocabTrainer😊
[查看演示（暂无）] | [报告问题] | [提出新功能]
> 这是我心血来潮做的一个小项目哒。原本是想进一步学习机器学习和强化学习的💪，但是突然想到自己还要学习英语，为什么不自己做一个程序去背英语单词呢？所以就开始着手啦😄

## ✨ 主要特性

- **📚 多词库支持**：内置IELTS词库，支持自定义词库扩展
- **🎯 智能学习**：随机单词抽取、模糊搜索、首字母分类
- **👤 用户管理**：多用户支持，个性化学习偏好设置
- **📊 学习统计**：记录学习进度、掌握程度、重点标记
- **🖥️ 图形界面**：基于PySide6的友好用户界面

## 🗂️ 文件结构
```text
VocabTrainer/
├── main.py              # 主程序入口
├── config.py            # 配置文件路径和默认设置
├── data_manager.py      # 数据管理和单词处理核心类
├── file_utils.py        # 文件操作工具函数
├── json_utils.py        # 用户数据JSON管理
├── utils.py             # 工具函数和初始化
├── test.py              # 功能测试脚本
├── login.py             # 登录和注册界面
└── data/
    ├── IELTS_2.json     # IELTS词库数据
    └── *.json           # 用户数据保存文件
```
## 🛠️ 技术栈

- **Python 3.10+** - 核心编程语言
- **Pandas** - 数据处理和分析
- **PySide6** - 图形用户界面
- **JSON** - 数据存储格式

## 🚀 快速开始

### 环境要求

- Python 3.10+[^1]
- 安装依赖包：
```bash
pip install pandas PySide6
```
[^1]: 在以下几个文件中使用了 match/case：
data_manager.py - search_word() 方法
json_utils.py - foucus_word_update() 方法
json_utils.py - output() 方法
如果版本低于python 3.10，需要修改match/case为if/elif/else


### 运行程序

```bash
python main.py
```

## 📖 使用说明

### 基本功能

1. **开始学习**：点击"开始学习"按钮随机显示单词
2. **查看详情**：点击"显示详细"查看单词的完整信息（例句、同义词、短语等）
3. **下一个单词**：点击"Next"切换到新单词
4. **单词搜索**：在搜索框中输入单词进行精确或模糊搜索

### 核心类说明


## 🔧 自定义配置

在 `config.py` 中可以调整程序设置：

```python
preferences = {
    'daily_words': 10,      # 每日学习单词数
    'background': 'dark',   # 界面主题
    'frequency': 1,         # 复习频率
    'review_mode': 'M'      # 复习模式 (L/M/H)
}
```

## 📈 数据源

目前的原始数据来自GitHub上的开源内容[^2]

[^2]: 数据源为：[kajweb/dict](https://github.com/kajweb/dict)

## 🧪 测试

运行测试脚本验证功能：

```bash
python test.py
```

## ✨ 代码概述
### 💾 数据处理
在找到重要的原始数据（.json格式），我采用了`pandas`去转换为`Dataframe`。
但是，在转换过后的数据中存在着大量的*非必要信息*，于是我根据`columns`手动筛选了重要的部分。
>`./file_utils.py`的`load_data`中通过iloc重新为df赋值，并新增了`'firstletter'`
```python
...
    df_ori = pd.json_normalize(d)
    df=df_ori.iloc[:,[0,1,5,13,16,21]]
    df.columns=['wordrank','word','sentences','synos','phrases','rels']
    df['firstletter']=df['word'].str[0]
```
### 🎯 基本功能编写
在处理好数据后，我开始着手编写`./data_manager`这一个文件
事实上，原本这个文件叫做`global_methods`，随后的许多函数和类也都是在一个文件中。
然而，我在具体调用后发现，如果想要项目具体清晰的实现功能，每一个文件负责一个大功能是比较理想的状态.询问了AI之后,我意识到一个分工明确的程序应当遵循：**单一职责原则 (Single Responsibility Principle)**和**关注点分离 (Separation of Concerns)**
| 名称       | 包含功能   | 不包含功能 |
|---|--|--|
| 数据层 (Data Layer)        | 只负责数据的存储、读取、序列化  | 不包含业务逻辑 |
| 业务层 (Business Layer)        | 包含核心的学习算法、用户管理逻辑  |  不直接处理UI或文件IO  |
| 表现层 (Presentation Layer)        | 只负责UI显示和用户交互  | 不包含业务逻辑  |

进而，我将`global_methods`拆分成`data_manager`和`json_utils`两个文件，分别管理数据分析和用户管理两个功能。
#### 核心类说明
##### `Data` 类 (`data_manager.py`)
单词数据处理的核心类，提供：
- 单词随机抽取 (`get_random_word`)
- 多种搜索模式 (`search_word`)
- 首字母分类 (`first_letter_divide`)
- 详细信息提取 (`get_details`)

##### `JsonManager` 类 (`json_utils.py`)
用户数据管理，功能包括：
- 用户账户创建和管理
- 学习进度记录
- 个性化偏好设置
- 重点单词标记


### 🔳 UI界面设计
目前的程序仅通过pyside去完成UI界面的交互，并且仅部分没有加入`./json_utils.py`的用户管理功能，预计将在后续跟进🎫

## 🔮 未来计划

- [x] 完善用户登录和个性化学习计划
- [ ] 添加单词发音功能
- [ ] 实现间隔重复算法
- [ ] 增加学习数据可视化
- [ ] 支持更多词库格式
- [ ] 添加单词测验功能
- [ ] 优化UI界面

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/YourFeature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送分支：`git push origin feature/YourFeature`
5. 提交 Pull Request

## 📞 联系我

如果你对我的代码有任何问题，或者有相关的内容想要跟我探讨，又或者想要和我一起学习编程/AI，欢迎联系！

- GitHub：`@Josh-Zhangccc`
- Email：`18136412760@163.com` 或 `zuoxiaozhang7@gmail.com`
- School：`CUHK(SZ)-SAI`

***

> **Note**: 这是一个学习项目，还在持续开发中。如果你有任何建议或发现了bug，欢迎反馈！💕

<!-- 链接定义 -->
[查看演示（暂无）]: https://github.com/Josh-Zhangccc/VocabTrainer/blob/main/docs/demo.gif
[报告问题]: https://github.com/Josh-Zhangccc/VocabTrainer/issues/new?template=bug_report.md
[提出新功能]: https://github.com/Josh-Zhangccc/VocabTrainer/issues/new?template=feature_request.md
