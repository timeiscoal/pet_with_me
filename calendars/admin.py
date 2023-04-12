from django.contrib import admin
from calendars.models import Challenge, UserChallenge , TodoCategory , ToDoList 

# Register your models here.

# 콘텐츠
@admin.register(Challenge)
class AdminChallenge(admin.ModelAdmin):
    pass

@admin.register(UserChallenge)
class AdminChellengeDay(admin.ModelAdmin):
    pass

# 댓글
@admin.register(TodoCategory)
class AdminTodoCategory(admin.ModelAdmin):
    pass

@admin.register(ToDoList)
class AdminToDoList(admin.ModelAdmin):
    list_display= ("title","date")