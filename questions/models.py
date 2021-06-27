from django.db import models
from mcqs.models import Test
from django.utils import timezone
# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all() #return all answers of a question

class Answer(models.Model):
    text = models. CharField(max_length=300)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return f"question: {self.question.text} answer: {self.text} correct: {self.correct}"
