from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListCreateView.as_view(), name='custommessage-list-create'),
    path('messages/<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='custommessage-detail'),
    path('my-messages/', views.UserMessagesListView.as_view(), name='user-messages'),
    path('messages-with/<int:user_id>/', views.ConversationBetweenUsersListView.as_view(), name='messages-with-user')
]
