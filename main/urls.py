from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path ,include



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('tools/', ),
    path('content/',include("contents.urls")),
    
    path('calendar/' , include("calendars.urls")),

    path('users/' , include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)