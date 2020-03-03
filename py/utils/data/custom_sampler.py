# -*- coding: utf-8 -*-

"""
@date: 2020/3/3 下午7:38
@file: custom_sampler.py
@author: zj
@description: 自定义采样器
"""

import numpy  as np
import random
from torch.utils.data import Sampler


class CustomSampler(Sampler):

    def __init__(self, num_positive, num_negative, batch_positive, batch_negative) -> None:
        """
        2分类数据集
        每次批量处理，其中batch_positive个正样本，batch_negative个负样本
        @param num_positive: 正样本数目
        @param num_negative: 负样本数目
        @param batch_positive: 单次正样本数
        @param batch_negative: 单次负样本数
        """
        self.num_positive = num_positive
        self.num_negative = num_negative
        self.batch_positive = batch_positive
        self.batch_negative = batch_negative

        length = num_positive + num_negative
        self.idx_list = list(range(length))

        self.batch = batch_negative + batch_positive
        self.num_iter = length // self.batch

    def __iter__(self):
        sampler_list = list()
        for i in range(self.num_iter):
            sampler_list.extend(random.shuffle(np.concatenate(
                (random.sample(self.idx_list[:self.num_positive], self.batch_positive),
                 random.sample(self.idx_list[self.num_positive:], self.batch_negative))
            )))
        return iter(sampler_list)

    def __len__(self) -> int:
        return self.num_iter * self.batch