from django.contrib import admin

from .models import ChatRoom, ChatMessage
from django import forms


class ChatRoomAdminForm(forms.ModelForm):
	class Meta:
		model = ChatRoom
		fields = ['room_number']

	def has_add_permission(self, request, *args, **kwargs):
		return False

	# def __init__(self, *args, **kwargs):
	# 	super(ChatRoomAdminForm, self).__init__(*args, **kwargs)
	# 	self.fields['tutor'].queryset = Account.objects.filter(role=Account.TUTOR, is_staff=False)
	# 	self.fields['student'].queryset = Account.objects.filter(role=Account.STUDENT, is_staff=False)



class ChatMessageInline(admin.TabularInline):
	model = ChatMessage
	extra = 0
	fields = ('sender','receiver','room_id','message','message_type','message_at','seen',)
	
	def get_readonly_fields(self, request, obj=None):
		readonly_fields = list(set(
			[field.name for field in self.opts.local_fields] +
			[field.name for field in self.opts.local_many_to_many]
		))
		
		return readonly_fields
	def has_add_permission(self, request, *args, **kwargs):
		return False


class ChatAdmin(admin.ModelAdmin):
	list_display = ['teacher','student', 'room_number']
	inlines = [ChatMessageInline]
	form = ChatRoomAdminForm

	# def booking(self, obj):
	# 	return obj.booking.id

	def teacher(self, obj):
		return obj.teacher.user.username

	def student(self, obj):
		return obj.student.username

	def has_add_permission(self, request, *args, **kwargs):
		return False
	def has_change_permission(self, request, *args, **kwargs):
		return False

		

admin.site.register(ChatRoom, ChatAdmin)

class ChatMessageListAdmin(admin.ModelAdmin):
	list_display = ('sender','receiver','room_id','message','message_type','message_at','seen',)
	def has_add_permission(self, request, *args, **kwargs):
		return False

admin.site.register(ChatMessage, ChatMessageListAdmin)