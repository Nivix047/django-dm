from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListCreateView.as_view(), name='custommessage-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='custommessage-detail')
]
