# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/5/21 14:27
# @Author : littleZhao
# @Site : 
# @File : train_ernie_tiny.py
# @Software : PyCharm
# Author:littleZhao
# -*- codeing = utf-8 -*-
# @Time : 2021/4/26 2:54
# @Author : littleZhao
# @Site :
# @File : trainer.py
# @Software : PyCharm

# 读取数据
import pandas as pd
import matplotlib.pyplot as plt

import os, io, csv
from paddlehub.datasets.base_nlp_dataset import InputExample, TextClassificationDataset

import paddlehub as hub
import paddle
from sklearn.model_selection import train_test_split

train_labled = pd.read_csv('data/nCoV_100k_train.labled.csv', engine='python', encoding='utf-8')
test = pd.read_csv('data/nCov_10k_test.csv', engine='python', encoding='utf-8')

print(train_labled.shape)
print(test.shape)
print(train_labled.columns)

# 清除异常标签数据
train_labled = train_labled[train_labled['情感倾向'].isin(["-1", "0", "1"])]

# 划分验证集，保存格式  text[\t]label
train_labled = train_labled[['微博中文内容', '情感倾向']]
train, valid = train_test_split(train_labled, test_size=0.2, random_state=2020)
train.to_csv('data/train.txt', index=False, header=False, sep='\t')
valid.to_csv('data/valid.txt', index=False, header=False, sep='\t')
# 标签分布


print(train_labled['微博中文内容'].str.len().describe())
# 选择模型
model = hub.Module(name="senta_bilstm", task='seq-cls', num_classes=3)  # 在多分类任务中，num_classes需要显式地指定类别数，此处根据数据集设置为3


# 自定义数据集


class MyDataset(TextClassificationDataset):
    # 数据集存放目录
    base_path = 'data/'
    # 数据集的标签列表
    label_list = ["-1", "0", "1"]

    def __init__(self, tokenizer, max_seq_len: int = 128, mode: str = 'train'):
        if mode == 'train':
            data_file = 'train.txt'
        elif mode == 'test':
            data_file = 'valid.txt'
        else:
            data_file = 'valid.txt'
        super().__init__(
            base_path=self.base_path,
            tokenizer=tokenizer,
            max_seq_len=max_seq_len,
            mode=mode,
            data_file=data_file,
            label_list=self.label_list,
            is_file_with_header=True)

    # 解析文本文件里的样本
    def _read_file(self, input_file, is_file_with_header: bool = False):
        if not os.path.exists(input_file):
            raise RuntimeError("The file {} is not found.".format(input_file))
        else:
            with io.open(input_file, "r", encoding="UTF-8") as f:
                reader = csv.reader(f, delimiter="\t", quotechar=None)
                examples = []
                seq_id = 0
                header = next(reader) if is_file_with_header else None
                for line in reader:
                    example = InputExample(guid=seq_id, text_a=line[0], label=line[1])

                    seq_id += 1
                    examples.append(example)
                return examples


train_dataset = MyDataset(model.get_tokenizer(), mode='train', max_seq_len=128)
dev_dataset = MyDataset(model.get_tokenizer(), mode='dev', max_seq_len=128)
test_dataset = MyDataset(model.get_tokenizer(), mode='test', max_seq_len=128)
for e in train_dataset.examples[:3]:
    print(e)

optimizer = paddle.optimizer.Adam(learning_rate=5e-5, parameters=model.parameters())  # 优化器的选择和参数配置
trainer = hub.Trainer(model, optimizer, checkpoint_dir='ckpt/', use_gpu=True)

trainer.train(train_dataset, epochs=3, batch_size=4, eval_dataset=dev_dataset, save_interval=1)  # 配置训练参数，启动训练，并指定验证集

result = trainer.evaluate(test_dataset, batch_size=32)  # 在测试集上评估当前训练模型
