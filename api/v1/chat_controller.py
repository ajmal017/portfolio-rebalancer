from rest_framework import generics
from api.v1.response_handler import response_handler, serialiser_errors
from rest_framework.response import Response
from modules.chat.models import ChatRoom
from django.utils.translation import ugettext_lazy as _
from rest_framework.pagination import LimitOffsetPagination
from .common_serializers import ChatMessageSerializer
from .common_serializers import *
from django.db.models import Q
from users.models import User
from modules.teacher.models import Teacher
import pdb


class GeChatRoomNumber(generics.GenericAPIView):
	def get(self, request, user):
		current_user = request.user
		second_user = user
		# if current_user.role == Account.TUTOR:
		# if current_user.is_teacher:
		# 	chat_room = ChatRoom.objects.filter(teacher=current_user.teacher, student_id=second_user)
		# 	if chat_room.exists():
		# 		chat_room = chat_room.first()
		# 	else:
		# 		chat_room = ChatRoom.objects.create(teacher=current_user.teacher, student_id=second_user)

		# else:
		# 	chat_room = ChatRoom.objects.filter(teacher_id=second_user, student=current_user)
		# 	if chat_room.exists():
		# 		chat_room = chat_room.first()
		# 	else:
		# 		chat_room = ChatRoom.objects.create(teacher_id=second_user, student=current_user)

		chat_room = ChatRoom.objects.filter(Q(student=current_user, teacher_id=second_user) | Q(teacher__user=current_user, student_id=second_user))
		if chat_room.exists():
			chat_room = chat_room.first()
		else:
			teacher = Teacher.objects.filter(id=second_user)
			if teacher.exists():
				chat_room = ChatRoom.objects.create(student=current_user, teacher_id=second_user)
			else:
				chat_room = ChatRoom.objects.create(teacher=current_user.teacher, student_id=second_user)

		return Response({'message': _('Chat room number fecthed successfully'), 'code': 200, 'data': {'room_number': chat_room.room_number, 'room_id': chat_room.id }})
		
class ChatCreateAPIView(generics.GenericAPIView):
	queryset = ChatMessage.objects.all()
	serializer_class = ChatCreateSerializer
	def post(self, request, *args, **kwargs):
		queryset = self.get_queryset()	
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			return response_handler(message=error_message, code=400,data={},error_message=error_message)
		self.object = serializer.save()
		chat_room = ChatRoom.objects.get(id=serializer.data['room_id'])
		if chat_room.student == request.user:
			sender = request.user
			receiver = chat_room.teacher.user
		else:
			sender = request.user
			receiver = chat_room.student
		chat_message = ChatMessage.objects.get(id=self.object.id)
		chat_message.sender = sender
		chat_message.receiver = receiver
		chat_message.save()
		message = "Chat created successfully"
		return response_handler(message=message, data={})



class ChatMessageList(generics.GenericAPIView):
	def get(self, request, room_number):
		try:
			chatroom = ChatRoom.objects.get(room_number=room_number)
			chat_message_list = chatroom.chatmessage_set.all().order_by('message_at')
			paginator = LimitOffsetPagination()
			queryset_serializer_data = paginator.paginate_queryset(chat_message_list, request)
			serializers = ChatMessageSerializer(queryset_serializer_data, many=True, context={'request': request})
			return Response({'message': _('Message fetched successfully'), 'code': 200, 'data': serializers.data, 'limit': paginator.limit,'offset': paginator.offset, 'overall_count': paginator.count})
		except Exception as ex:
			return Response({'message': str(ex), 'code': 500, 'data': []})