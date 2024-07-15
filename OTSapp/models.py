from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Candidates(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(null=False, max_length=20)
    name = models.CharField(null=False, max_length=30)

    def __str__(self) -> str:
        return self.name

class Test(models.Model):
    TestName = models.CharField(max_length=100)
    total_questions = models.IntegerField(null=True, blank=True)
    test_description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.TestName

class TestQuestions(models.Model):
    TestName = models.ForeignKey(Test, on_delete=models.CASCADE)
    Question = models.TextField()
    Op1 = models.CharField(max_length=100)
    Op2 = models.CharField(max_length=100)
    Op3 = models.CharField(max_length=100)
    Op4 = models.CharField(max_length=100)
    rightAns = models.CharField(max_length=100)

    def __str__(self) -> str:
        return  f"{self.Question} ----> {self.TestName}"
    

class Result(models.Model):
    username = models.ForeignKey(Candidates, on_delete=models.CASCADE)
    TestName = models.ForeignKey(Test, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    right = models.IntegerField()
    wrong = models.IntegerField()
    point = models.IntegerField()