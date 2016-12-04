import nltk
from matplotlib import pyplot
from nltk import ConditionalFreqDist
from numpy import arange

colors = 'rgbcmyk'

def bar_chart(categories, words, counts):
    "Plot a bar chart showing counts for each word by category"
    ind = arange(len(words))
    width = 1 / (len(categories) + 1)
    bar_groups = []
    for c in range(len(categories)):
        bars = pyplot.bar(ind+c*width, counts[categories[c]], width,
                         color=colors[c % len(colors)])
        bar_groups.append(bars)
    pyplot.xticks(ind+width, words)
    pyplot.legend([b[0] for b in bar_groups], categories, loc='upper left')
    pyplot.ylabel('Frequency')
    pyplot.title('Frequency of Six Modal Verbs by Genre')
    pyplot.show()
# def bar_chart(categories, words, counts):
#     '''
#     Plot bar chart for each category.
#     :param categories:
#     :param words:
#     :param counts:
#     :return:
#     '''
#     import pylab
#     ind = pylab.arange(len(words))
#     width = 1 / (len(categories) + 1)
#     bar_groups = []
#     for c in range(len(categories)):
#         bars = pylab.bar(ind + c * width, counts[categories[c]], width,
#                          color=colors[c % len(colors)])
#         bar_groups.append(bars)
#     pylab.xticks(ind + width, words)
#     pylab.legend([b[0] for b in bar_groups], categories, loc='upper left')
#     pylab.ylabel('Frequency')
#     pylab.title('Frequency of Six Modal Verbs by Genre')
#     pylab.show()

genres = ['news', 'religion', 'hobbies', 'government', 'adventure']
modals = ['can', 'could', 'may', 'might', 'must', 'will']
cfdist = ConditionalFreqDist(
    (genre, word)
    for genre in genres
    for word in nltk.corpus.brown.words(categories=genres)
    if word in modals)
counts = {}
for genre in genres:
    counts[genre] = [cfdist[genre][word] for word in modals]
bar_chart(genres, modals, counts)
