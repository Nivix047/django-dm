from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from users.models import CustomUser
from .models import FriendRequest, FriendList
from .serializers import FriendRequestSerializer, CustomUserSerializer


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Retrieve the ID of the receiver from the request data.
        receiver_id = request.data.get('receiver_id')

        if receiver_id:
            try:
                # Fetch the receiver user instance.
                receiver = CustomUser.objects.get(pk=receiver_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Create and save the friend request.
            FriendRequest.objects.create(
                sender=request.user, receiver=receiver)
            return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Receiver ID required"}, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Retrieve the ID of the friend request from the request data.
        friend_request_id = request.data.get('friend_request_id')

        if friend_request_id:
            try:
                # Fetch the friend request instance.
                friend_request = FriendRequest.objects.get(
                    pk=friend_request_id)
            except FriendRequest.DoesNotExist:
                return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

            # Ensure both sender and receiver have a friend list.
            friend_list_sender, _ = FriendList.objects.get_or_create(
                user=friend_request.sender)
            friend_list_receiver, _ = FriendList.objects.get_or_create(
                user=friend_request.receiver)

            # Add each other to their respective friend lists.
            friend_list_sender.friends.add(friend_request.receiver)
            friend_list_receiver.friends.add(friend_request.sender)

            # Delete the original friend request.
            friend_request.delete()

            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)

        return Response({"error": "FriendRequest ID required"}, status=status.HTTP_400_BAD_REQUEST)


class DeclineFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Retrieve the ID of the friend request from the request data.
        friend_request_id = request.data.get('friend_request_id')

        if friend_request_id:
            try:
                # Fetch the friend request instance.
                friend_request = FriendRequest.objects.get(
                    pk=friend_request_id)
            except FriendRequest.DoesNotExist:
                return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

            # Delete the friend request.
            friend_request.delete()
            return Response({"message": "Friend request declined"}, status=status.HTTP_200_OK)

        return Response({"error": "FriendRequest ID required"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Retrieve the ID of the friend to be deleted from the request data.
        friend_id = request.data.get('friend_id')

        if friend_id:
            try:
                # Fetch the friend user instance.
                friend = CustomUser.objects.get(pk=friend_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                # Fetch the friend list of the authenticated user.
                friend_list = FriendList.objects.get(user=request.user)
            except FriendList.DoesNotExist:
                return Response({"error": "FriendList not found for the user"}, status=status.HTTP_404_NOT_FOUND)

            # Remove the friend from the user's friend list and vice versa.
            friend_list.remove_friend(friend)
            friend_user_friend_list = FriendList.objects.get(user=friend)
            friend_user_friend_list.remove_friend(request.user)

            return Response({"message": "Friend removed successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Friend ID required"}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Fetch all the friend requests for the authenticated user.
        friend_requests = FriendRequest.objects.filter(receiver=request.user)
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Fetch the friend list of the authenticated user.
            friend_list = FriendList.objects.get(user=request.user)
        except FriendList.DoesNotExist:
            return Response({"error": "FriendList not found for the user"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all friends from the friend list.
        friends = friend_list.friends.all()
        serializer = CustomUserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
