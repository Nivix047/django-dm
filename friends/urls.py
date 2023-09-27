from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, DeclineFriendRequestView, ListFriendRequestsView

urlpatterns = [
    path('send-friend-request/', SendFriendRequestView.as_view(),
         name='send-friend-request'),
    path('accept-friend-request/', AcceptFriendRequestView.as_view(),
         name='accept-friend-request'),
    path('decline-friend-request/', DeclineFriendRequestView.as_view(),
         name='decline-friend-request'),
    path('list-friend-requests/', ListFriendRequestsView.as_view(),name='list-friend-requests')
]
