from django.db import models
from users.models import User

# Create your models here.

# 카테고리
class Category(models.Model):


    name = models.CharField(max_length=100, null=True)



    # 관리자들이 작성한 콘텐츠 
class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    discription = models.TextField()
    likes = models.ManyToManyField(User , blank=True ,related_name="content_like")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    categories = models.ForeignKey(Category, null=True,blank=True, on_delete=models.SET_NULL)
    contents_view = models.IntegerField(default=0 , null=True, blank=True)
    images = models.ImageField(upload_to="%Y", blank=True, null=True,)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # 작성자가 탈퇴하면 댓글도 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 콘텐츠가 삭제되면 댓글도 삭제
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    discription = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __strt__(self):
        return self.content.title

# class ImageModel(models.Model):

#     image = models.ImageField(upload_to="%Y", blank=True, null=True,)
#     content =models.ForeignKey(Content,on_delete=models.CASCADE,null=True,blank=True , related_name="images")

#     def __str__(self):
#         return self.content.title