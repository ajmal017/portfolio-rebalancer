from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from django.conf import settings
from .models import ChatRoom, ChatMessage as Message
from .exceptions import ClientError
from .utils import get_room_or_error, create_message, load_message_json, get_receiver
# from web_services.api.serializers import ChatMessageSerializer
from api.v1.common_serializers import ChatMessageSerializer
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from .utils import get_user
from urllib import parse


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    # async def connect(self):
    #     """
    #     Called when the websocket is handshaking as part of initial connection.
    #     """
    #     # Are they logged in?
    #     try:
    #         self.token_key = self.scope['url_route']['kwargs']['token']
    #         if self.token_key:
    #             token = Token.objects.get(key=self.token_key)
    #             self.scope['user'] = token.user
    #         else:
    #             self.scope['user'] = AnonymousUser()

    #         if self.scope["user"].is_anonymous:
    #             # Reject the connection
    #             await self.close()
    #         else:
    #             # Accept the connection
    #             await self.accept()
    #         # Store which rooms the user has joined on this connection
    #     except Exception as ex:
    #         print("Exception")
    #         print(ex)
        
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # query_string = dict(self.scope).get('query_string')
        # keys = dict(parse.parse_qs(query_string.decode()))
        self.token_key = self.scope['url_route']['kwargs']['token']
        try:
            if self.token_key:
                # access_token = keys.get('key')
                print(self.token_key)
                self.scope['user'] = await get_user(self.token_key)
                # self.chat_room = self.scope['url_route']['kwargs']['channel']
                await self.accept()

        except Exception as ex:
            print("Exception", ex)
            self.scope['user'] = AnonymousUser()
            await self.close()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        try:
            print(content)
            command = content.get("command", None)
            if command == "join":
                await self.join_room(content["room"])

            elif command == "leave":
                await self.leave_room(content["room"])

            elif command == "send":
                await self.send_room(content)

            elif command == "upload":
                await self.upload_room(content)

        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        await self.close()

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                    "sender": self.scope["user"].id,
                }
            )
        
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": room.room_number,
            "sender": self.scope["user"].id,
        })

    ##### Command helper methods called by receive_json

    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"])
        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                    "sender": self.scope["user"].id,
                }
            )
        
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the room
        await self.send_json({
            "join": room.room_number,
            "title": room.room_number,
            "sender": self.scope["user"].id,
        })

    async def send_room(self, content):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        
        room = await get_room_or_error(content['room'], self.scope["user"])
        # if self.scope["user"].role == 'STUDENT':
        #     receiver = room.tutor
        # else:
        #     receiver = room.student
        try:
            receiver = await get_receiver(self.token_key)
        except Exception as ex:
            print(ex)
        # mesg_obj = Message.objects.create(
        #     sender=self.scope['user'],
        #     message=content.get('message','Loading..'),
        #     room_id=room,
        #     message_type=content.get('message_type','TEXT'),
        #     receiver_id=118)
        mesg_obj = await create_message(room, self.scope["user"], content)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "message_id": mesg_obj.id
            }
        )

    async def upload_room(self, content):
        print(content)
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(content['room'], self.scope["user"])
        if self.scope["user"].role == 'STUDENT':
            receiver = room.tutor
        else:
            receiver = room.student

        mesg_obj = Message.objects.create(
            sender=self.scope['user'],
            media_url=content.get('file',None),
            message=content.get('message',"Uploading.."),
            room_id=room,
            message_type=content.get('message_type','IMAGE'),
            receiver=receiver)

        # Send a join message if it's turned on
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.upload",
                "message_id": mesg_obj.id
            }
        )
        
    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    
    async def chat_upload(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        serializer = await load_message_json(event['message_id'])
        await self.send_json(
            serializer,
        )

    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "room": event["room_id"],
                "username": event["username"],
                "sender":  event["sender"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "room": event["room_id"],
                "username": event["username"],
                "sender":  event["sender"],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        serializer = await load_message_json(event['message_id'])
        print(serializer)
        await self.send_json(
            serializer,
        )


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = self.room_name
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         room_id = text_data_json['room_id']
#         message_type = text_data_json['message_type']
#         receiver = text_data_json['receiver']
#         message_at = text_data_json['message_at']
#         # Send message to room group
#         if not message:
#             return
#         room = ChatRoom.objects.get(id=room_id)
#         Message.objects.create(
#             sender=self.scope['user'],
#             message=message,
#             room_id=room,
#             message_type=message_type,
#             receiver_id=receiver,
#             message_at=message_at)

#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'user': self.scope['user'].email,
#                 'message_at': message_at
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#         message_at = event['message_at']
#         user = event['user']
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message,
#             'user': user,
#             'message_at': message_at,
#         }))
