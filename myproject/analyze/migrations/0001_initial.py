# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=2047)),
                ('link', models.URLField(max_length=2047)),
                ('content', models.TextField(blank=True)),
                ('date_modified', models.DateTimeField()),
                ('author', models.CharField(max_length=255, blank=True)),
                ('tags', models.TextField(blank=True)),
                ('summary', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Section`',
                'verbose_name_plural': 'Sections',
            },
        ),
        migrations.AddField(
            model_name='feed',
            name='section',
            field=models.ForeignKey(verbose_name='Sections', to='analyze.Section'),
        ),
        migrations.AddField(
            model_name='article',
            name='feed',
            field=models.ForeignKey(verbose_name='feed', to='analyze.Feed'),
        ),
    ]
