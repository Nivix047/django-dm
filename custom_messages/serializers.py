from rest_framework import serializers
from .models import CustomMessage     

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMessage        
        fields = ('id', 'sender', 'recipient', 'content', 'timestamp')
