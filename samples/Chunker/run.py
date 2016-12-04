#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-12-4 下午8:48
# @Author  : sadscv
# @File    : run.py

from ConsecutiveNPChunkTagger import ConsecutiveNPChunker

if __name__ == '__main__':

    # 需要加上这两句才能使用megam算法。
    from nltk.classify import megam
    megam.config_megam('./megam.opt')

    from nltk.corpus import conll2000

    #将conll2000中的分块类型为NP的句子选为测试集。
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    #创建分类器。
    chunker = ConsecutiveNPChunker(test_sents)
    #打印评分。
    print(chunker.evaluate(test_sents))
