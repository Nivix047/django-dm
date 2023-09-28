from django.urls import path
from .views import (CreateGroupView, SendGroupInvitationView, AcceptGroupInvitationView,
                    SendGroupMessageView, ListGroupInvitationsView, ListGroupMessagesView, ListGroupsView, DeclineGroupInvitationView, LeaveGroupView)

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
         ListGroupMessagesView.as_view(), name='list-messages'),
    path('group/', ListGroupsView.as_view(), name='list-groups'),
    path('decline-invitation/', DeclineGroupInvitationView.as_view(),
         name='decline-invitation'),
    path('leave-group/', LeaveGroupView.as_view(), name='leave-group')
]
