from rest_framework import serializers
from .models import Group, GroupMessage, GroupInvitation


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = '__all__'


class GroupInvitationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    group = GroupSerializer()

    class Meta:
        model = GroupInvitation
        fields = '__all__'
