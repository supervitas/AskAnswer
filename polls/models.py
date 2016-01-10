from django.db import models
from django.contrib.auth.models import User, UserManager


class MyModelManager(models.Manager):
    def get_new_queryset(self):
        return super(MyModelManager, self).get_queryset().order_by('-created')

    def get_best_queryset(self):
        return super(MyModelManager, self).get_queryset().order_by('-rating')


class CustomUser(User):
    avatar = models.ImageField()
    objects = UserManager()


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)


class LikeForQuestion(models.Model):
    value = models.IntegerField()
    question_related = models.ForeignKey('Question', null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("question_related", "user"),)

    def __unicode__(self):
        return '%s  voted on %s' % (self.user, self.question_related.title)

    objects = models.Manager()
    manager = MyModelManager()


class LikeForAnswers(models.Model):
    value = models.IntegerField()
    answer_related = models.ForeignKey('Answer', null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("answer_related", "user"),)

    def __unicode__(self):
        return '%s  voted on %s' % (self.user, self.answer_related.title)

    objects = models.Manager()
    manager = MyModelManager()


class Question(models.Model):
    title = models.TextField()
    content = models.TextField()
    created = models.DateTimeField()
    author = models.ForeignKey(CustomUser, related_name="author_of_q")
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, through=LikeForQuestion, blank=True, related_name='likes_for_q')

    objects = models.Manager()
    manager = MyModelManager()


class Answer(models.Model):
    created = models.DateTimeField()
    question = models.ForeignKey(Question, null=True)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, related_name='author_of_a')
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    likes = models.ManyToManyField(CustomUser, through=LikeForAnswers, blank=True, related_name='likes_for_a')


class Logic:

    @staticmethod
    def get_tag(tag):
        testtag = Tag.objects.filter(title=tag)
        if testtag:
            return Question.manager.get_best_queryset().filter(tags__title__exact=tag)
        else:
            return Question.objects.none()

    @staticmethod
    def get_order(question):
        return question.answer_set.order_by('-rating', '-created')
    @staticmethod
    def get_new_qs(question):
        return question.answer_set.order_by('-created')

