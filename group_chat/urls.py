from django.urls import path
from .views import (CreateGroupView, SendGroupInvitationView, AcceptGroupInvitationView,
                    SendGroupMessageView, ListGroupInvitationsView, ListGroupMessagesView)

urlpatterns = [
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('send-invitation/', SendGroupInvitationView.as_view(),
         name='send-invitation'),
    path('accept-invitation/', AcceptGroupInvitationView.as_view(),
         name='accept-invitation'),
    path('send-message/', SendGroupMessageView.as_view(), name='send-message'),
    path('list-invitations/', ListGroupInvitationsView.as_view(),
         name='list-invitations'),
    path('list-messages/<int:group_id>',
         ListGroupMessagesView.as_view(), name='list-messages')
]
