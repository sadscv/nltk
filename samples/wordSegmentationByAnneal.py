# 将文本根据segs分词
from random import randint


def segment(text, segs):
    words = []
    last = 0
    for i in range(len(segs)):
        if '1' == segs[i]:
            words.append(text[last:i+1])
            last = i + 1
    words.append(text[last:])
    return words

# 评估当前segs分词效果
def evaluate(text, segs):
    words = segment(text, segs)
    text_size = len(words)
    lexicion_size = len(' '.join(list(set(words))))
    # print('text_size:%s, lexicion_size:%s' % (text_size, lexicion_size))
    return text_size + lexicion_size

# 变异seg在当前pos的值
def flip(segs, pos):
    return segs[:pos] + str(1 - int(segs[pos])) + segs[pos + 1:]

def flip_n(segs, n):
    for i in range(n):
        segs = flip(segs, randint(0, len(segs) - 1))
    return segs

# 模拟退火求最佳分词
def anneal(text, segs, iterations, cooling_rate):
    temperature = float(len(segs))
    while temperature > 0.5:
        best_segs, best = segs, evaluate(text, segs)
        for i in range(iterations):
            guess = flip_n(segs, int(round(temperature)))
            score = evaluate(text, guess)
            if score < best:
                print('score:%s, guess:%s' % (score, guess))
                best, best_segs = score, guess
        score, segs = best, best_segs
        temperature = temperature / cooling_rate
        print(temperature, evaluate(text, segs), segment(text, segs))
    print()
    return segs

if __name__ == '__main__':
    text = 'doyouseethekittyseethedoggydoyoulikethekittylikethedoggy'
    seg1 = '0000000000000001000000000010000000000000000100000000000'
    anneal(text, seg1, 5000, 1.2)