from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.v1.common_serializers import *
from api.v1.response_handler import response_handler, serialiser_errors
from modules.teacher.models import Teacher
from modules.enquiry.models import Enquiry
from modules.configurations.models import StaticPages, Ratings
from modules.booking.models import Booking
from modules.payment.models import PaymentDue
import pdb

class TeacherListingAPIView(generics.ListAPIView):
	permission_classes = (AllowAny,)
	serializer_class = TeacherListSerializer

	def get_queryset(self):
		if self.request.user.username:
			qs = Teacher.objects.filter(is_verified=True).exclude(user=self.request.user)
		else:
			qs = Teacher.objects.filter(is_verified=True)
		return qs

	def list(self, request):
		serializers = self.serializer_class(self.get_queryset(), many=True).data
		message = "Teachers list fetched successfully" 
		return response_handler(message=message, data=serializers)

class TeacherDetailAPIView(generics.RetrieveAPIView):
	permission_classes = (AllowAny,)
	queryset = Teacher.objects.all()
	serializer_class = TeacherDetailSerializer
	def get(self, request, pk):
		query_obj = self.get_object()
		serializer = self.serializer_class(query_obj)
		message = "Teacher detail fetched successfully"
		return response_handler(message=message, data=serializer.data)


class EnquiryCreateAPIView(generics.CreateAPIView):
	permission_classes = (AllowAny,)
	serializer_class = EnquiryCreateSerializer
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			message = "Failed"
			return response_handler(message=message, error_message=error_message, code=500)
		queryset = super().create(request, *args, **kwargs)
		message = "Thank you for contacting us"	
		return response_handler(message=message, data=queryset.data)

class StaticPageAPIView(generics.GenericAPIView):
	permission_classes = (AllowAny,)
	def get(self, request):
		page = request.GET.get('q', False)
		if page:
			static_page = StaticPages.objects.filter(template_name__icontains=page).first()
			static_page = UserStaticPageSerializer(static_page).data
			message = "Static page fetched successfully"
			return response_handler(message=message, data=static_page)
		else:
			message = "Please make sure you pass all details"
			return response_handler(message=message)

class ShareMediaAPIView(generics.CreateAPIView):
	serializer_class = ShareMediaSerializer
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			error_message = serialiser_errors(serializer)
			message = "Failed"
			return response_handler(message=message, error_message=error_message, code=500)
		queryset = super().create(request, *args, **kwargs)
		message = "Media shared successfully"
		return response_handler(message=message, data=queryset.data)

class ShareMediaVideo(generics.GenericAPIView):
	def post(self, request, pk):
		# pdb.set_trace()
		if request.data.get('video_file'):
			media = Media.objects.get(id=pk)
			media.video_file = request.data.get('video_file')
			media.save()
			queryset = ShareMediaSerializer(media)
			message = "Media shared successfully"
			return response_handler(message=message, data=queryset.data)
		else:
			message = "Not found"
			return response_handler(message=message, data={}, error_message=message)


class SubmitReviewAPIView(generics.CreateAPIView):
	queryset = Ratings.objects.all()
	serializer_class = RatingReviewSerializer
	def create(self, request, *args, **kwargs):
		queryset = super().create(request, *args, **kwargs)
		message = "Review submitted successfully"
		return response_handler(message=message, data=queryset.data)

class BookingMarkCompleteAPIView(generics.GenericAPIView):
	def post(self, request, booking):
		booking = Booking.objects.filter(id=booking).first()
		if booking.student == request.user:
			booking.student_satisfy = True
			booking.save()
		else:
			if not booking.media_set.filter(shared_by="TEACHER").exists():
				message = "You did not shared any media to mark this booking as complete"
				return response_handler(code=400, message=message, error_message=message)
			booking.teacher_satisfy = True
			booking.save()
		if booking.student_satisfy and booking.teacher_satisfy:
			booking.booking_status = "COMPLETED"
			teacher = booking.teacher
			price = booking.price
			booking.save()
			PaymentDue.objects.create(booking=booking, amount=price)
		message = "Booking Status Updated"
		return response_handler(message=message, data={})

