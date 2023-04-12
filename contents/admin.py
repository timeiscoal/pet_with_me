from django.contrib import admin
from contents.models import Comment, Content , Category
# Register your models here.

# 콘텐츠
@admin.register(Content)
class AdminContent(admin.ModelAdmin):
    pass

# 댓글
@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    pass

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass

# @admin.register(ImageModel)
# class AminImageModel(admin.ModelAdmin):
#     pass