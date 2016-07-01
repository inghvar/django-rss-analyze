from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from bs4 import BeautifulSoup
import re

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk import FreqDist
from nltk.corpus import stopwords
from collections import Counter

from .models import Article, Feed

def index(request):
    words_all = all_words()
    most_common_words = most_words()
    return render_to_response('index.html',
            {'all_words': words_all,
             'most_common_words': most_common_words,},
            context_instance=RequestContext(request))


def news(request):
    pass

html_text = []

""" the func prepare out text """
def prepare():
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

text = prepare()

def all_words():
    word_tokens = word_tokenize(text)
    count = Counter(word_tokens)
    return count.most_common(15)


def most_words():
    stop_words = set(stopwords.words('english')) # set stop words
    word_tokens = word_tokenize(text)
    filtered = [w for w in word_tokens if not w in stopwords.words('english')]
    count = Counter(filtered)
    return count.most_common(15)
    #for w in word_tokens:
    #    if w not in stop_words:
    #        filtered_words.append(w)
    #fdict = FreqDist(filtered_words)
    #most_common_words = fdict.most_common(15)
    #return most_common_words


    


