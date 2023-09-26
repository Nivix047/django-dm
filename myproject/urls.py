from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path('api/messages/', include('custom_messages.urls')),   
    path('password_reset/', include('django.contrib.auth.urls')),
]
