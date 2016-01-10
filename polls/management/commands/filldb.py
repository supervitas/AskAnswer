# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from random import randint, randrange
from datetime import timedelta, datetime
from loremipsum import get_sentence, get_paragraphs
from polls.models import Question, Answer, Tag, LikeForAnswers, LikeForQuestion, CustomUser
import pytz
import django.db

users_count = 101
questions_count = 100
answers_count = 1000
tags_count = 100
votes_count = 200


class Command(BaseCommand):
  help = 'Filling database with data'

  def handle(self, *args, **options):
    start_time = datetime.now()
    #Заполнение юзеров
    for user_id in range(1, users_count + 1):
      user = CustomUser(
          avatar='default.jpg',
          password=make_password("password"),
          last_login=self.random_date(),
          is_superuser=False,
          username="user%s" % (user_id),
          first_name="",
          last_name="",
          email="",
          is_staff=False,
          is_active=True,
          date_joined=datetime(2015, 1, 1, 1, 0, 0, 0, pytz.UTC)
      )
      self.stdout.write("User#%d" % user_id)
      user.save()
    # Заполнение вопросов
    for question_id in range(1, questions_count + 1):
      text = ''
      for i in get_paragraphs(randint(1, 4)):
        text += i

      question = Question(
          title=get_sentence(),
          content=text,
          author_id=randint(1, users_count),
          created=self.random_date(),
          rating=0
      )
      self.stdout.write("Question#%d" % question_id)
      question.save()

    # Заполнение ответов
    for answer_id in range(1, answers_count + 1):
      text = ''
      for i in get_paragraphs(randint(1, 2)):
        text += i

      answer = Answer(
          id=answer_id,
          content=text,
          author_id=randint(1, users_count),
          created=self.random_date(),
          question_id=randint(1, questions_count),
          rating=0
      )

      self.stdout.write("Answer#%d" % answer_id)
      answer.save()

    # Заполнение тэгов
    words = open('polls/words', 'r')
    for tag_id in range(1, tags_count + 1):
      tag = Tag(title=words.readline()[:-1])
      tag.save()
    words.close()


   # Заполнение лайков вопросов
    for like_id in range(1, votes_count):
      l_value = randint(0, 1)
      if l_value == 0:
        l_value = -1
      rand_user = randint(1, users_count)
      rand_question = randint(1, questions_count)
      try:
        like = LikeForQuestion(user_id=rand_user, value=l_value, question_related_id=rand_question)
        like.save()
        self.stdout.write("Like#%d" % like_id)
        quest = Question.objects.get(id=rand_question)
        quest.rating = str(l_value + quest.rating)
        quest.save()
      except django.db.IntegrityError:
          pass


    # Для ответов
    for like_id in range(1, votes_count):
      l_value = randint(0, 1)
      if l_value == 0:
        l_value = -1
      rand_user = randint(1, users_count)
      rand_question = randint(1, questions_count)
      try:
        like = LikeForAnswers(user_id=rand_user, value=l_value, answer_related_id=rand_question)
        like.save()
        self.stdout.write("Like#%d" % like_id)
        quest = Answer.objects.get(id=rand_question)
        quest.rating = str(l_value + quest.rating)
        quest.save()
      except django.db.IntegrityError:
          pass

    # Добавление тегов к вопросам
    for question_id in range(1, questions_count + 1):
      question = Question.objects.get(pk=question_id)
      self.stdout.write("Linking tags#%d" % question_id)
      for i in range(1, 4):
        question.tags.add(Tag.objects.get(pk=randint(1, tags_count)))

    end_time = datetime.now()
    self.stdout.write(
        'Database filled successfully' + str(end_time - start_time))

  def random_date(self):
    start = datetime(2015, 1, 1, 1, 0, 0, 0, pytz.UTC)
    end = datetime(2016, 1, 1, 1, 0, 0, 0, pytz.UTC)

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
