from django.contrib import admin
from .models import *


class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)



class FeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'is_active')
    list_filter = ('name',)
    search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_modified',)
    search_fields = ('title',)


admin.site.register(Section, SectionAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Article, ArticleAdmin)
