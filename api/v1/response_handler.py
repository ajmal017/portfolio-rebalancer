from rest_framework.response import Response

def response_handler(code=200, message="", error_message="", data={}):
	return Response({'code': code, 'message': message, 'data': data, 'error_message': error_message})

def serialiser_errors(serializer):
	error_message = " & ".join([str(serializer.errors.get(error)[0]) for error in serializer.errors])
	return error_message