from rest_framework.views import exception_handler
from rest_framework.response import Response
import pdb
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == 401:
            return Response({'message': "Incorrect authentication details, Please check whether you are login or not.", 'code': response.status_code, 'data': response.data.get('detail'), 'error_message': response.data.get('detail','Login required')})
        elif response.status_code == 400:

            #if len(response.data.get('non_field_errors')) > 0:
            error_message = ''
            for error in response.data:
                #pdb.set_trace()
                error_message += error.title()+":"+response.data[error][0]+","
            #pdb.set_trace()
            return Response({'message':"Vaildation error occer",'code':response.status_code,'data':{},'error_message':error_message.rstrip(',')})
        else:            
            return Response({'message': "Something went wrong, check error message for more details.", 'code': response.status_code, 'data': response.data.get('detail'), 'error_message': response.data.get('detail','A server error occurred')})
    return response
