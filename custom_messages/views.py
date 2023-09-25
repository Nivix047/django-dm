from rest_framework import generics, permissions
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
