from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from django.db.models import Q  
from .models import CustomMessage    
from .serializers import MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = CustomMessage.objects.all()    
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageRetrieveUpdateDestroyView(mixins.RetrieveModelMixin, 
                                       mixins.DestroyModelMixin, 
                                       mixins.UpdateModelMixin, 
                                       generics.GenericAPIView):
    queryset = CustomMessage.objects.all()   
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
      response = self.destroy(request, *args, **kwargs)
      if response.status_code == status.HTTP_204_NO_CONTENT:
          return Response({"message": "Message deleteed successfully"}, status=status.HTTP_200_OK)
      return response

    def patch(self, request, *args, **kwargs):  # Only PATCH allowed
        return self.partial_update(request, *args, **kwargs)

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
