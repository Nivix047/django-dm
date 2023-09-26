from django.urls import path
from . import views

urlpatterns = [
    path('', views.MessageListCreateView.as_view(), name='custommessage-list-create'),
    path('<int:pk>/', views.MessageRetrieveUpdateDestroyView.as_view(), name='custommessage-detail'),
    path('my-messages/', views.UserMessagesListView.as_view(), name='user-messages'),  # changed 'my-messages/' to 'my/'
    path('messages-with/<int:user_id>/', views.ConversationBetweenUsersListView.as_view(), name='messages-with-user')  # changed 'messages-with/' to 'with/'
]

