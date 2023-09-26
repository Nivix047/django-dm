from rest_framework import serializers
from .models import CustomMessage     

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomMessage        
        fields = ('id', 'sender', 'recipient', 'content', 'timestamp')
        read_only_fields = ('id', 'sender', 'timestamp')  

    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        if self.instance:  # checks if the serializer is being used for updates
            self.fields['recipient'].read_only = True
