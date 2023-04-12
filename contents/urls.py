from django.urls import path ,include
from contents import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register('test/test', views.PostViewSet)


urlpatterns = [
    # path("",include(router.urls)),

    
    path("api/v1/", views.ConetntView.as_view()),
    path('api/v1/conetnt/create/<int:user_id>/', views.ContentCreateView.as_view()),

    path('api/v2/<int:content_id>/', views.ContentDetailView.as_view()),
    path('api/v2/<int:content_id>/like/', views.ContentsLikeView.as_view()),
    path('api/v2/<int:content_id>/comment/', views.CommentView.as_view()),
    path('api/v2/<int:content_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view()),

    path("api/v3/categorylist/", views.TestViewSet.as_view()),

    path("api/v3/category/", views.CategoryView.as_view()),
    path("api/v3/category/<int:category_id>", views.CategoryDetailView.as_view())
    
    

] 
