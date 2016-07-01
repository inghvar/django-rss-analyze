from django.db import models

class Section(models.Model):
    title = models.CharField(max_length=150, verbose_name=u'Title')

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u'Section`'
        verbose_name_plural = u'Sections'
        ordering = ('title',)


class Feed(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, verbose_name=u'Sections')
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.url



class Article(models.Model):

    feed = models.ForeignKey(Feed, verbose_name=u'feed')
    title = models.CharField(max_length=2047)
    link = models.URLField(max_length=2047)
    content = models.TextField(blank=True)
    date_modified = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    tags = models.TextField(blank=True)
    summary = models.TextField(blank=True)


    def __unicode__(self):
        return self.title
