# -*- coding: utf-8 -*-
# http://www.quora.com/With-Google-News-API-going-away-what-is-the-best-option-for-company-news-search-feed
# http://www.faroo.com/hp/api/api.html#description
# http://developer.usatoday.com/
# http://developer.nytimes.com/
# http://open-platform.theguardian.com/
# http://news.google.com/news?q=politics&output=rss
# http://open-platform.theguardian.com/explore/
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

import sys
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

import django
django.setup()

import feedparser

from analyze.models import Feed
from analyze.models import Article

from datetime import datetime
import time
from django.utils import timezone
from time import mktime

if __name__ == "__main__":

    feeds = Feed.objects.all().filter(is_active=True)

    for article in Article.objects.all():
            article.delete()



    def ParseFeed():
        for feed in feeds:
            for i in range(0, 200):
                d = feedparser.parse(str(feed))
                try:
                    title = d['entries'][i]['title']
                except (KeyError, IndexError):
                    pass
                try:
                    link = d['entries'][i]['link']
                except (KeyError, IndexError):
                    pass
                try:
                    author = d['entries'][i]['author']
                except (KeyError, IndexError):
                    pass
                try:
                    summary = d['entries'][i]['summary']
                except (KeyError, IndexError):
                    pass
                try:
                    content = d['entries'][i]['content'][i].value
                except (KeyError, IndexError):
                    pass
                try:
                    tags = d['entries'][i]['tags'][i].term
                except (KeyError, IndexError):
                    pass

                b = Article()
                try:                    
                    b.title = title
                except UnboundLocalError:
                    pass
                try:
                    b.link = link
                except UnboundLocalError:
                    pass
                try:
                    b.feed = feed
                    b.date_modified = datetime.fromtimestamp(mktime(d['entries'][i].published_parsed) - time.timezone, timezone.get_current_timezone())
                except (IndexError, AttributeError):
                    b.date_modified = datetime.now()
                try:
                    b.content = content
                except UnboundLocalError:
                    pass
                try:
                    b.summary = summary
                except UnboundLocalError:
                    pass
                try:
                    b.tags = tags
                except UnboundLocalError:
                    pass
                try:              
                    b.author = author
                except UnboundLocalError:
                    pass
                if Article.objects.filter(title=title):
                    pass
                else:
                    b.save()
        print "Import complete"


    ParseFeed()
