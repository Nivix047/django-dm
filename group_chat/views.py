from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Group, GroupInvitation, GroupMessage
from .serializers import GroupSerializer, GroupMessageSerializer, GroupInvitationSerializer
from users.models import CustomUser

# Create new group


class CreateGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get group name and recipients from the request data
        group_name = request.data.get("group_name")
        recipient_ids = request.data.get(
            "recipient_ids", [])  # List of user IDs to invite

        # Validate if group name exists
        if not group_name:
            return Response({"error": "Group name required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate recipient_ids to ensure it's provided as a list
        if not recipient_ids or not isinstance(recipient_ids, list):
            return Response({"error": "Recipient IDs must be provided as a list"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the group and add the authenticated user as a member
        group = Group.objects.create(name=group_name)
        group.members.add(request.user)

        # Gather all the recipients from provided recipient_ids
        recipients = []
        for r_id in recipient_ids:
            try:
                recipient = CustomUser.objects.get(pk=r_id)
                recipients.append(recipient)
            except CustomUser.DoesNotExist:
                group.delete()  # Delete the group if an invalid recipient is found
                return Response({"error": f"Recipient with ID {r_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Send group invitations to all recipients
        for recipient in recipients:
            if not GroupInvitation.objects.filter(sender=request.user, recipient=recipient, group=group).exists():
                GroupInvitation.objects.create(
                    sender=request.user, recipient=recipient, group=group)

        return Response({"message": "Group created and invitations sent successfully", "group_id": group.id}, status=status.HTTP_201_CREATED)

# Send group invitation


class SendGroupInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get group ID and recipient IDs from the request data
        recipient_ids = request.data.get('recipient_ids', [])
        group_id = request.data.get('group_id')

        # Validate recipient_ids and group_id
        if not recipient_ids or not isinstance(recipient_ids, list):
            return Response({"error": "Recipient IDs must be provided as a list"}, status=status.HTTP_400_BAD_REQUEST)
        if not group_id:
            return Response({"error": "Group ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the group exists
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Gather all the recipients
        recipients = []
        for r_id in recipient_ids:
            try:
                recipient = CustomUser.objects.get(pk=r_id)
                recipients.append(recipient)
            except CustomUser.DoesNotExist:
                return Response({"error": f"Recipient with ID {r_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Send group invitations to all recipients
        for recipient in recipients:
            if not GroupInvitation.objects.filter(sender=request.user, recipient=recipient, group=group).exists():
                GroupInvitation.objects.create(
                    sender=request.user, recipient=recipient, group=group)

        return Response({"message": "Invitations sent successfully"}, status=status.HTTP_201_CREATED)

# Accept group invitation


class AcceptGroupInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get the invitation ID from the request data
        invitation_id = request.data.get('invitation_id')

        if not invitation_id:
            return Response({"error": "Invitation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the invitation exists and hasn't been accepted yet
        try:
            invitation = GroupInvitation.objects.get(
                pk=invitation_id, recipient=request.user, accepted=False)
        except GroupInvitation.DoesNotExist:
            return Response({"error": "Invitation not found or already accepted"}, status=status.HTTP_404_NOT_FOUND)

        # Mark the invitation as accepted and add the user to the group members
        invitation.accepted = True
        invitation.save()
        invitation.group.members.add(request.user)

        return Response({"message": "Invitation accepted successfully"}, status=status.HTTP_201_CREATED)

# Send group message


class SendGroupMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Get group ID and message content from the request data
        group_id = request.data.get('group_id')
        content = request.data.get('content')

        # Validate the provided data
        if not group_id or not content:
            return Response({"error": "Group and content are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the group exists
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure that the authenticated user is a member of the group
        if request.user not in group.members.all():
            return Response({"error": "User not a member of the group"}, status=status.HTTP_403_FORBIDDEN)

        # Create the group message
        GroupMessage.objects.create(
            sender=request.user, group=group, content=content)

        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)

# List al group invitations


class ListGroupInvitationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all unaccepted group invitations for the authenticated user
        invitations = GroupInvitation.objects.filter(
            recipient=request.user, accepted=False)
        serializer = GroupInvitationSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# List all group messages


class ListGroupMessagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        # Check if the group exists and the user is a member
        try:
            group = Group.objects.get(pk=group_id)
            if request.user not in group.members.all():
                return Response({"error": "User not a member of the group"}, status=status.HTTP_403_FORBIDDEN)

            # Get all messages for the given group
            messages = GroupMessage.objects.filter(group=group)
            serializer = GroupMessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

# List all groups the user is a member of


class ListGroupsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Filter groups where the user is a member
        groups = Group.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Decline group invitation


class DeclineGroupInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        invitation_id = request.data.get('invitation_id')

        if not invitation_id:
            return Response({"error": "Invitation ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = GroupInvitation.objects.get(
                pk=invitation_id, recipient=request.user, accepted=False)
        except GroupInvitation.DoesNotExist:
            return Response({"error": "Invitation not found or already accepted/declined"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the invitation to signify that it has been declined
        invitation.delete()

        return Response({"message": "Invitation declined successfully"}, status=status.HTTP_200_OK)
