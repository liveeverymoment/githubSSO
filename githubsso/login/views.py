"""
Views for login app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import hashlib
from django.shortcuts import redirect 
from urllib.parse import urlencode 
from githubsso import settings
from login.models import CustomerOptions
from login.models import Oidcclient
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt,name='dispatch')
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

    def post(self,request):
        """
        Initiates SSO for configured IDP.
        """
        print('inside post.')
        state=hashlib.md5((settings.SECRET_KEY).encode('utf-8').hexdigest())
        customer_objects=CustomerOptions.objects.get(key='oauthappname')
        oauthapp=customer_objects.value
        oidc_object=Oidcclient.objects.get(application_name=oauthapp)
        data={
            "client_id":oidc_object.client_id,
            "redirect_uri":oidc_object.redirect_uri,
            "response_type":oidc_object.response_type,
            "state":state,
            "scope":oidc_object.scope
        }
        query_string=urlencode(data)
        authorization_endpoint=oidc_object.authorization_endpoint
        url=f'{authorization_endpoint}?{query_string}'
        print(f'url:: {url}')
        response=redirect(url)
        response["Access-Control-Allow-Origin"]="*"
        response["Access-Control-Allow-Methods"]="GET"
        response.status_code=302
        return response

class GetAccessCodeView(APIView):
    """
    Receive access code from idp.
    """
    def get(self,request):
        """
        Receive code.
        """
        code=request.query_params.GET('code')
        state=request.query_params.GET('state')
        state_original=hashlib.md5((settings.SECRET_KEY).encode('utf-8').hexdigest())
        if(str(state)==str(state_original)):
            pass
        else:
            return None