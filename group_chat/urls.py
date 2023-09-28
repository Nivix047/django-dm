from django.urls import path
from .views import CreateGroupView, SendGroupInvitationView, AcceptGroupInvitationView, SendGroupMessageView

urlpatterns = [
    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('send-invitation/', SendGroupInvitationView.as_view(),
         name='send-invitation'),
    path('accept-invitation/', AcceptGroupInvitationView.as_view(),
         name='accept-invitation'),
    path('send-message/', SendGroupMessageView.as_view(), name='send-message'),
]
