from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class HostMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.META['HTTP_HOST'] + request.META['PATH_INFO']
        if host == 'dabbawala.com.mx/' or host == 'www.dabbawala.com.mx/':
            return redirect('users:new_customer')
