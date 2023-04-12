from django.db import models
from users.models import User

# Create your models here.

# 목록 카테고리
class TodoCategory(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

# 해야 할 리스트
class ToDoList(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(TodoCategory ,on_delete=models.CASCADE)
    discription = models.CharField(max_length=100)
    date= models.CharField(max_length=30)
    update_date= models.DateField(auto_now=True)
    is_works = models.BooleanField(default=False , blank=True)


# 챌린지/목표(카테고리 개념)
class Challenge(models.Model):
    name = models.CharField(max_length=100 , null=True , blank=True)
    discription = models.CharField(max_length=100, null=True,blank=True)
    image = models.ImageField(upload_to="media",null=True,blank=True)

    def __str__(self) -> str:
        return self.name

# 오늘 하루 성공 여부 / 도전 중
class UserChallenge(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    mychallenge = models.ForeignKey(Challenge, on_delete=models.CASCADE )
    today_is_work = models.BooleanField(default=False,blank=True)
    complete = models.BooleanField(default=False , blank=True)
    count = models.PositiveIntegerField(default=0,blank=True)
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)


