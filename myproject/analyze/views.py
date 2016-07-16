from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from bs4 import BeautifulSoup
import re

import nltk
import nltk.classify.util
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk import FreqDist
from nltk.corpus import stopwords
from collections import Counter
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

from .models import Article, Feed

def index(request):
    articles = Article.objects.all()[:30]
    words_all = all_words()
    most_common_words = most_words()
    return render_to_response('index.html',
            {'all_words': words_all,
             'most_common_words': most_common_words,
             'articles': articles},
            context_instance=RequestContext(request))


def article(request, pk):
    twit = analyze_one_twit(pk)
    return render_to_response('article.html',
            {'twit': twit},
            context_instance=RequestContext(request))

html_text = []

""" the func prepare out text """
def prepare_all_text():
    st = Article.objects.all()
    # remove html tag
    for s in st:
        html_text.append(s.summary)
    soup = BeautifulSoup(str(html_text), "html.parser")
    raw_text = soup.get_text()
    # remove non letter
    raw_text = re.sub(r"\\'", "'", raw_text)
    raw_text = re.sub("[^a-zA-Z']", " ", raw_text)
    # remove 'u'
    raw_text = re.sub("u", "", raw_text)
    # remove whitespace
    raw_text = re.sub(r"  ", " ", raw_text)
    raw_text = re.sub(r"   ", " ", raw_text)
    raw_text = re.sub("' ", "", raw_text)
    raw_text = re.sub(" '", "", raw_text)
    # convert to lower case
    raw_text = raw_text.strip().lower()
    return raw_text


def all_words():
    word_tokens = word_tokenize(prepare_all_text())
    count = Counter(word_tokens)
    return count.most_common(15)


def most_words():
    stop_words = set(stopwords.words('english')) # set stop words
    word_tokens = word_tokenize(prepare_all_text())
    filtered = [w for w in word_tokens if not w in stopwords.words('english')]
    count = Counter(filtered)
    return count.most_common(15)
    #for w in word_tokens:
    #    if w not in stop_words:
    #        filtered_words.append(w)
    #fdict = FreqDist(filtered_words)
    #most_common_words = fdict.most_common(15)
    #return most_common_words

def word_feats(words):
    return dict([(word, True) for word in words])


def analyze_one_twit(pk):
    articl = Article.objects.get(id=pk)

    data_clean = articl.summary.decode('utf-8')
    sents = nltk.tokenize.sent_tokenize(data_clean)

    words = []
    for sent in sents:
        words += nltk.tokenize.wordpunct_tokenize(sent)

    test = word_feats(words)

    print articl.title + " : " + classifier.classify(test)
    return articl.title + " : " + classifier.classify(test)


negative_ids = movie_reviews.fileids('neg')
positive_ids = movie_reviews.fileids('pos')

negative_features = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negative_ids]
positive_features = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in positive_ids]

# Split our total data set (2000 reviews) into 3rds: 2/3rds we will use to train,
# the remaining 1/3rd we will use to test
# note that the positive set and the negative set are both cut into 2/3 : 1/3 divisions
negcutoff = len(negative_features)*2/3
poscutoff = len(positive_features)*2/3

# Assemble the  training and testing features into their own list
train_features = negative_features[:negcutoff] + positive_features[:poscutoff]
test_features = negative_features[negcutoff:] + positive_features[poscutoff:]

classifier = NaiveBayesClassifier.train(train_features)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test_features)
classifier.show_most_informative_features()