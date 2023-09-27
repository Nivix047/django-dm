from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from users.models import CustomUser
from .models import FriendRequest, FriendList
from .serializers import FriendRequestSerializer


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')
        if receiver_id:
            try:
                receiver = CustomUser.objects.get(pk=receiver_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            FriendRequest.objects.create(
                sender=request.user, receiver=receiver)
            return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Receiver ID required"}, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        friend_request_id = request.data.get('friend_request_id')
        if friend_request_id:
            try:
                friend_request = FriendRequest.objects.get(
                    pk=friend_request_id)
            except FriendRequest.DoesNotExist:
                return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

            # Create FriendList for both users if it doesn't exist
            friend_list_sender, _ = FriendList.objects.get_or_create(
                user=friend_request.sender)
            friend_list_receiver, _ = FriendList.objects.get_or_create(
                user=friend_request.receiver)

            # Add each other to their respective friend lists
            friend_list_sender.friends.add(friend_request.receiver)
            friend_list_receiver.friends.add(friend_request.sender)

            # Delete the friend request
            friend_request.delete()

            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        return Response({"error": "FriendRequest ID required"}, status=status.HTTP_400_BAD_REQUEST)


class DeclineFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        friend_request_id = request.data.get('friend_request_id')
        if friend_request_id:
            try:
                friend_request = FriendRequest.objects.get(
                    pk=friend_request_id)
            except FriendRequest.DoesNotExist:
                return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

            friend_request.delete()
            return Response({"message": "Friend request declined"}, status=status.HTTP_200_OK)
        return Response({"error": "FriendRequest ID required"}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friend_requests = FriendRequest.objects.filter(receiver=request.user)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
