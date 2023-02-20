"""
Views for login app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from login.models import CustomerOptions

class LoginAPIView(APIView):
    """
    API view for login page.
    """
    renderer_classes=(TemplateHTMLRenderer,)
    
    def get(self,request):
        customer_object=CustomerOptions.objects.get(key='oauthserver')
        oauthserver=customer_object.value
        data={
            'IDP':oauthserver
        }
        return Response(template_name='login/login.html',data=data)
