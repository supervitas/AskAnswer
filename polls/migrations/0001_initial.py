# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('content', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(upload_to=b'')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LikeForAnswers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('answer_related', models.ForeignKey(to='polls.Answer', null=True)),
                ('user', models.ForeignKey(to='polls.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='LikeForQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('created', models.DateTimeField()),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(related_name='author_of_q', to='polls.CustomUser')),
                ('likes', models.ManyToManyField(related_name='likes_for_q', through='polls.LikeForQuestion', to='polls.CustomUser', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='polls.Tag'),
        ),
        migrations.AddField(
            model_name='likeforquestion',
            name='question_related',
            field=models.ForeignKey(to='polls.Question', null=True),
        ),
        migrations.AddField(
            model_name='likeforquestion',
            name='user',
            field=models.ForeignKey(to='polls.CustomUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(related_name='author_of_a', to='polls.CustomUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(related_name='likes_for_a', through='polls.LikeForAnswers', to='polls.CustomUser', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='polls.Question', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='likeforquestion',
            unique_together=set([('question_related', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='likeforanswers',
            unique_together=set([('answer_related', 'user')]),
        ),
    ]
