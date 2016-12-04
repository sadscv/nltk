#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-12-4 下午8:52
# @Author  : sadscv
# @File    : chunkFreatures.py


def npchunk_features(sentence, i, history):
    """
    特征抽取器

    :param sentence:(word,tag)
    :param i: int, 当前sentence第i个词
    :param history: i前所有的tag(chunk)
    :return:{"pos":pos}
    """

    word, pos = sentence[i]
    return {"pos": pos}


def npchunk_features_with_prevword_and_prevpos(sentence, i, history):
    """
    在npchunk_feature的基础上添加word, prevpos两个特征。

    :param sentence:
    :param i:
    :param history:
    :return:
    """
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    return {"pos":pos, "word":word, "prevpos":prevpos}


def tags_since_dt(sentence, i):
    """

    :param sentence:(word,tag)
    :param i: int, 当前sentence第i个词
    :return:i前一个定冠词到i之后的pos.
    例如 he is the little lovely boy.NN, DT,( JJ, JJ, NN)则返扩号中的内容。
    """
    tags = set()

    #对于i之前的每个(word,pos)
    for word, pos in sentence[:i]:
        #如果pos是‘DT’，则将tags清空。否则添加当前pos.
        if pos =='DT':
            tags = set()
        else:
            tags.add(pos)
    return ('+'.join(sorted(tags)))

def npchunk_features_ultimate(sentence, i, history):
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    if i == len(sentence)-1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i+1]
    return {
        "pos" : pos,
        "word" : word,
        "prevpos" : prevpos,
        "nextpos" : nextpos,
        "tags-since-dt" : tags_since_dt(sentence, i),
        # "prevpos+pos": "%s+%s" % (prevpos, pos),
        # "pos+nextpos": "%s+%s" % (pos, nextpos),
    }