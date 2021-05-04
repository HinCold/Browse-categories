# coding: UTF-8
from importlib import import_module
import pickle as pkl
import train_eval
import numpy as np
import torch
from utils import DatasetIterater
UNK, PAD = '<UNK>', '<PAD>'


def configInit():
    dataset = 'THUCNews'  # 数据集

    # 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
    embedding = 'embedding_SougouNews.npz'
    model_name = 'TextCNN'

    x = import_module('models.' + model_name)
    config = x.Config(dataset, embedding)
    # np.random.seed(1)
    # torch.manual_seed(1)
    # torch.cuda.manual_seed_all(1)
    # torch.backends.cudnn.deterministic = True  # 保证每次结果一样
    # print("config:***************************")
    # config.device = 'cpu'
    # print(config.device)
    return x, config


def getDataIter(text, config):
    text = text.strip()
    tokenizer = lambda x: [y for y in x]
    token = tokenizer(text)
    # print(token)

    pad_size = config.pad_size
    words_line = []
    seq_len = len(token)
    if pad_size:
        if len(token) < pad_size:
            token.extend([PAD] * (pad_size - len(token)))
        else:
            token = token[:pad_size]
            seq_len = pad_size

    vocab = pkl.load(open(config.vocab_path, 'rb'))
    # print(f"Vocab size: {len(vocab)}")

    # word to id
    for word in token:
        words_line.append(vocab.get(word, vocab.get(UNK)))
    contents = []

    contents.append((words_line, 0, seq_len))
    # contents.append((words_line, int(label), seq_len, bigram, trigram))
    # contents = [(words_line, seq_len)]

    iterate = DatasetIterater(contents, config.batch_size, config.device)
    iterate.residue = True
    return iterate, vocab


if __name__ == '__main__':
    x, config = configInit()
    text = "高考学习更加紧张"
    iterate, vocab = getDataIter(text, config)
    config.n_vocab = len(vocab)
    model = x.Model(config).to(config.device)
    # print("model:****************")
    # print(model.parameters)
    p = train_eval.predict(config, model, iterate)
    print(p)
