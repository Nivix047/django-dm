from rest_framework import serializers
from .models import CustomMessage     

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMessage        
        fields = ('id', 'sender', 'recipient', 'content', 'timestamp')

    # def create(self, validated_data):
    #     validated_data['sender'] = self.context['request'].user
    #     return super().create(validated_data)
