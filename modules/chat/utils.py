from channels.db import database_sync_to_async
from datetime import datetime
from .exceptions import ClientError
from .models import ChatRoom, ChatMessage
# from web_services.api.serializers import ChatMessageSerializer
from api.v1.common_serializers import ChatMessageSerializer
from rest_framework.authtoken.models import Token
# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html

@database_sync_to_async
def get_user(access_token):
    try:
        token = Token.objects.get(key=access_token)
    except Token.DoesNotExist:
        raise ClientError("TOKEN_INVALID")
    return token.user


@database_sync_to_async
def get_receiver(access_token):
    try:
        token = Token.objects.get(key=access_token)
    except Token.DoesNotExist:
        raise ClientError("TOKEN_INVALID")
    return token.user


@database_sync_to_async
def get_room_or_error(room_number, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user or not user.is_authenticated:
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = ChatRoom.objects.get(room_number=room_number)
    except ChatRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room


@database_sync_to_async
def create_message(room, user,content):
    try:
        mesg_obj = ChatMessage.objects.create(
            sender=user,
            message=content.get('message','Loading..'),
            room_id=room,
            message_type=content.get('message_type','TEXT'),
            receiver_id=118)
    except:
        raise ClientError("ROOM_INVALID on message")
    return mesg_obj

    # try:
    #     if user == room.owner:
    #         receiver = room.guest
    #     else:
    #         receiver = room.owner

    #     mesg_obj = ChatMessage.objects.create(
    #         sender=user,
    #         message=content.get('message',''),
    #         room=room,
    #         receiver=receiver)
    # except:
    #     raise ClientError("ROOM_INVALID on message")
    # return mesg_obj


@database_sync_to_async
def load_message_json(pk):
    try:
        mesg_obj = ChatMessage.objects.get(pk=pk)
        messages=  ChatMessageSerializer(mesg_obj).data
    except:
        raise ClientError("ROOM_INVALID on message load")
    return messages