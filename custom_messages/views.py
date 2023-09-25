from rest_framework import generics, permissions
from django.db.models import Q  
from .models import CustomMessage    
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = CustomMessage.objects.all()    
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomMessage.objects.all()   
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CustomMessage.objects.filter(Q(sender=user) | Q(recipient=user))

class ConversationBetweenUsersListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user1 = self.request.user
        user2_id = self.kwargs['user_id']
        return CustomMessage.objects.filter(
            Q(sender=user1, recipient__id=user2_id) | 
            Q(sender__id=user2_id, recipient=user1)
        )
