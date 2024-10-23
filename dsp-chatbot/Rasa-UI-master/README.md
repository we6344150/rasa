# Rasa-UI
A simple Rasa UI

![a.gif](https://i.loli.net/2020/06/18/KEG1atwnScQFIgV.gif)

# 使用方法
1. 创建rasa环境
```bash
conda create –n rasa python=3.10.14 #虚拟环境名叫rasa3，限定Python版本
```

2. 激活rasa3
```bash
conda activate rasa
```

3. 安装rasa、安装rasa-sdk、安装Jieba分词器
```bash
pip install rasa  
pip install rasa-sdk
pip install rasa[jieba]

```

4. 初始化Rasa
```bash
mkdir C:/work/project #创建项目工作目录
cd C:/work/project
rasa init
```
随便建一个目录执行rasa init然后把项目文件复制进去

4. 配置 endpoints.yml
```
# 配置 endpoints.yml
action_endpoint:
  url: "http://localhost:5054/webhook"
 
# 配置 config.yml
language: zh

pipeline:
- name: "JiebaTokenizer"  # 添加Jieba分词器，需要先安装`rasa[jieba]`
- name: "CountVectorsFeaturizer"  # 特征提取器，适用于基于词袋模型的特征表示
- name: "DIETClassifier"  # 强大的意图分类器，同时也支持实体识别
  epochs: 100  # 可根据实际情况调整
  constrain_similarities: true
policies:
- name: "MemoizationPolicy"
- name: "TEDPolicy"
  max_history: 5    # 考虑的对话轮数
  epochs: 100
  batch_size: 32
  embedding_dimension: 256
  lr_multiplier: 1.0
- name: "RulePolicy"
```

5. 训练rasa
```bash
rasa train
```

6. 启动Rasa API（允许跨域、输出debug级别日志）
```bash
rasa run --port 5054 --enable-api --cors "*" --debug
```

7. 启动Rasa action（输出debug级别日志）
```bash
rasa run actions --port 5054 --debug
```
8. 直接打开页面`index.html`

rasa run --enable-api --cors "*" --debug

rasa run actions --debug


