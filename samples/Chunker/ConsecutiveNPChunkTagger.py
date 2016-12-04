#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk


def npchunk_features(sentence, i, history):
    """

    :param sentence:(word,tag)
    :param i: int, 当前sentence第i个词
    :param history: i前所有的tag(trunk)
    :return:
    """
    word, pos = sentence[i]
    return {"pos": pos}


class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        """
        :
        将tagger用作chunker.因此分类器中所有的tag都是chunk.
        :param train_sents:((word,tag),chunk)
        """
        train_set = []

        #对每个训练集中的句子
        for tagged_sent in train_sents:

            # param untagged_sent: 生成untag(即untrunk)句子集合。
            untagged_sent = nltk.tag.untag(tagged_sent)

            #param history: 当前句中第i个词之前的所有tag(trunk)
            history = []

            # 对于每个句子中的每个词，提取出其特征，并将特征加入train_set。
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                #history中加入之前的tag(trunk)
                history.append(tag)

        # 创建最大熵分类器并用train_set训练。
        self.classifier = nltk.MaxentClassifier.train(
            train_set, algorithm='megam', trace=3)

    def tag(self, sentence):
        """

        :param sentence: (word,tag)
        :return:((word,tag),chunk)
        """
        #history为该句中i之前的词的chunk.
        history = []

        #对每个单词，提取特征，并用分类器分类。将分类逐个加入history中，
        #最后将sentence和history zip一下。变为((w,t),c)形式。
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)





class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        """

        :param train_sents:训练集
        """

        #将训练集从树转为conll2000格式再转为((word,tag),chunk)格式。
        tagged_sents = [[((w,t),c) for (w,t,c) in \
                         nltk.chunk.tree2conlltags(sent)] for sent in
                        train_sents]

        #实例化一个tagger，并用tagged_sents训练。
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)


    def parse(self, sentence):
        """

        :param sentence:被用来分类的测试语句。
        :return: conll2000格式转变成的tree.
        """

        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)


if __name__ == '__main__':

    from nltk.classify import megam
    megam.config_megam('./megam.opt')

    from nltk.corpus import conll2000
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    chunker = ConsecutiveNPChunker(test_sents)
    print(chunker.evaluate(test_sents))
    # # nltk.download()
