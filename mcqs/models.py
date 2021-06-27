from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import random
from django.utils import timezone

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=500)
    number_of_questions = models.IntegerField()
    time = models.IntegerField()
    passing_score = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions) # for random order of questions
        return questions[:self.number_of_questions] #return all questions

    def get_absolute_url(self):
        return reverse('mcqs:main-view')
