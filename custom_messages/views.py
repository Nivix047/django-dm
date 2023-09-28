from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from django.db.models import Q
from .models import CustomMessage
from .serializers import MessageSerializer

# Endpoint to list all messages and create a new message


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = CustomMessage.objects.all()  # All messages will be listed
    serializer_class = MessageSerializer
    # Only authenticated users can access
    permission_classes = [permissions.IsAuthenticated]

    # Overrides the save method to automatically set the sender to the current user
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# Endpoint to retrieve, update, and delete a specific message


class MessageRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.UpdateModelMixin,
                                       generics.GenericAPIView):
    queryset = CustomMessage.objects.all()
    serializer_class = MessageSerializer
    # Only authenticated users can access
    permission_classes = [permissions.IsAuthenticated]

    # Retrieve a specific message
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # Delete a specific message and provide custom response on successful deletion
    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Message deleted successfully"}, status=status.HTTP_200_OK)
        return response

    # Partially update a specific message (only fields provided will be updated)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# Endpoint to list all messages sent or received by the current user


class UserMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filter messages to only include those sent or received by the current user
    def get_queryset(self):
        user = self.request.user
        return CustomMessage.objects.filter(Q(sender=user) | Q(recipient=user))

# Endpoint to list all messages between the current user and another specified user


class ConversationBetweenUsersListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filter messages to only include those between the current user and the specified user
    def get_queryset(self):
        user1 = self.request.user
        user2_id = self.kwargs['user_id']
        return CustomMessage.objects.filter(
            Q(sender=user1, recipient__id=user2_id) |
            Q(sender__id=user2_id, recipient=user1)
        )
