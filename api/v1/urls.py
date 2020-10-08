from django.urls import path, include, re_path
from .auth_controller import *
from .home import *
from .chat_controller import *

urlpatterns = [
	path('auth/login', Login.as_view()),
	path('teacher-listing', TeacherListingAPIView.as_view()),
	path('teacher-detail/<int:pk>', TeacherDetailAPIView.as_view()),
	path('auth/sign-up', SignUpAPIView.as_view()),
	re_path('auth/activate', ActivateAccountAPIView.as_view(), name="activation"),
	path('auth/forget-password', ForgetPasswordAPIView.as_view()),
	path('auth/role-update', RoleUpdateAPIView.as_view()),
	# , name="forget-password"
	re_path('auth/reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', ResetUserPasswordView.as_view(), name="reset-password"),
	path('auth/change-password', ChangePassword.as_view()),
	path('send-enquiry', EnquiryCreateAPIView.as_view(), name="send-enquiry"),
	path('student/',include('api.v1.students.urls')),
	path('teacher/',include('api.v1.teachers.urls')),
	path('static-pages', StaticPageAPIView.as_view(), name="static-page"),
	# path('')
	path('share-media', ShareMediaAPIView.as_view(), name="share-media"),
	path('share-media-video/<int:pk>', ShareMediaVideo.as_view()),
	path('signup-initial',InitialRegistrationView.as_view()),
	path('notifications/',include('api.v1.notifications.urls')),
	path('payment/', include('api.v1.payments.urls')),
	path('submit/review', SubmitReviewAPIView.as_view(), name="submit-review"),
	path('get-chat-room-number/<int:user>/',GeChatRoomNumber.as_view(),),
	path('create-chat', ChatCreateAPIView.as_view()),
	path('get-chat-messages/<str:room_number>',ChatMessageList.as_view(),),
	path('booking-mark-complete/<int:booking>', BookingMarkCompleteAPIView.as_view())
    

]