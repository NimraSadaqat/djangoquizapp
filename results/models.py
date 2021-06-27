from django.db import models
from mcqs.models import Test
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Result(models.Model):
    test_name = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_date_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
