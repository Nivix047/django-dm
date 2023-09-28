from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Group, GroupInvitation, GroupMessage
from .serializers import GroupSerializer, GroupMessageSerializer
from users.models import CustomUser


class CreateGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        group_name = request.data.get("group_name")
        # Expecting a list of user IDs to invite
        recipient_ids = request.data.get("recipient_ids", [])

        if not group_name:
            return Response({"error": "Group name required"}, status=status.HTTP_400_BAD_REQUEST)

        if not recipient_ids or not isinstance(recipient_ids, list):
            return Response({"error": "Recipient IDs must be provided as a list"}, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.create(name=group_name)
        group.members.add(request.user)

        # Gather all the recipients
        recipients = []
        for r_id in recipient_ids:
            try:
                recipient = CustomUser.objects.get(pk=r_id)
                recipients.append(recipient)
            except CustomUser.DoesNotExist:
                # If one of the recipient_ids is invalid, we can delete the group and return an error.
                group.delete()  # Cleanup: delete the group since we're not moving forward with invitations
                return Response({"error": f"Recipient with ID {r_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Now, create invitations for all the recipients
        for recipient in recipients:
            if not GroupInvitation.objects.filter(sender=request.user, recipient=recipient, group=group).exists():
                GroupInvitation.objects.create(
                    sender=request.user, recipient=recipient, group=group)

        return Response({"message": "Group created and invitations sent successfully", "group_id": group.id}, status=status.HTTP_201_CREATED)


class SendGroupInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Expecting a list of user IDs
        recipient_ids = request.data.get('recipient_ids', [])
        group_id = request.data.get('group_id')

        if not recipient_ids or not isinstance(recipient_ids, list):
            return Response({"error": "Recipient IDs must be provided as a list"}, status=status.HTTP_400_BAD_REQUEST)

        if not group_id:
            return Response({"error": "Group ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        recipients = []
        for r_id in recipient_ids:
            try:
                recipient = CustomUser.objects.get(pk=r_id)
                recipients.append(recipient)
            except CustomUser.DoesNotExist:
                return Response({"error": f"Recipient with ID {r_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Now, create invitations for all the recipients
        for recipient in recipients:
            if not GroupInvitation.objects.filter(sender=request.user, recipient=recipient, group=group).exists():
                GroupInvitation.objects.create(
                    sender=request.user, recipient=recipient, group=group)

        return Response({"message": "Invitations sent successfully"}, status=status.HTTP_201_CREATED)


class AcceptGroupInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        invitation_id = request.data.get('invitation_id')
        if not invitation_id:
            return Response({"error": "Invitation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = GroupInvitation.objects.get(
                pk=invitation_id, recipient=request.user, accepted=False)
        except GroupInvitation.DoesNotExist:
            return Response({"error": "Invitation not found or already accepted"}, status=status.HTTP_404_NOT_FOUND)

        invitation.accepted = True
        invitation.save()
        invitation.group.members.add(request.user)

        return Response({"message": "Invitation accepted successfully"}, status=status.HTTP_201_CREATED)


class SendGroupMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        group_id = request.data.get('group_id')
        content = request.data.get('content')
        if not group_id or not content:
            return Response({"error": "Group and content are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in group.members.all():
            return Response({"error": "User not a member of the group"}, status=status.HTTP_403_FORBIDDEN)

        GroupMessage.objects.create(
            sender=request.user, group=group, content=content)

        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)
