from django.urls import path 
from calendars import views

urlpatterns = [
    
    path("challenge/" , views.ChallengeListView.as_view()),
    path("challenge/<int:challenge_id>/", views.ChallengeDetailView.as_view()),

    path("challenge/mychallenge/<int:user_id>",views.MyChallengeListView.as_view()),
    path("challenge/create/<int:user_id>/" , views.UserCreateChallengeView.as_view()),

    path("challenge/user/<int:user_id>/challenge/<userchallenge_id>/" , views.UserChallengeDetailPageView.as_view()),
    path("challenge/user/<int:user_id>/detail/<userchallenge_id>/" , views.UserChallengeDetailView.as_view()),


    path('<int:user_id>/todolist/', views.TodoListAllView.as_view()),
    path('<int:user_id>/todolist/detail/<todo_day>/' ,views.ToDoListView.as_view()),

    path("<int:user_id>/todolist/create/" ,views.TodoCategoryCreate.as_view()),
    path("<int:user_id>/todolist/category/", views.ToDoListCategoryView.as_view()),

    path("<int:user_id>/todolist/day/<int:todo_id>/detail" , views.ToDoListDetailView.as_view()),

    
    
    
    path("<int:user_id>/todolist/day/<todo_day>/detail/<int:todo_id>/work/", views.ToDolistWorkView.as_view()),
    
    # path('<todo_day>/' , views.ToDoListView.as_view()),
    # path('<todo_day>/create/' ,views.TodoCategoryCreate.as_view()),
    # path("<todo_day>/detail/<todo_id>/" , views.ToDoListDetailView.as_view()),
    # path("<todo_day>/detail/<todo_id>/work/" , views.ToDolistWorkView.as_view()),

]

