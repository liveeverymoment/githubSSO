"""
Views for login app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import hashlib
import json
import logging
import requests
from django.shortcuts import redirect 
from urllib.parse import urlencode 
from django.shortcuts import get_object_or_404
from githubsso import settings
from login.models import CustomerOptions
from login.models import Oidcclient
from users.models import User

LOGGER=logging.getLogger(__file__)

class LoginAPIView(APIView):
    """
    API view for login page.
    """
    renderer_classes=(TemplateHTMLRenderer,)
    template_name='login/login.html'
    
    def get(self,request,pk):
        user=get_object_or_404(User,pk=pk)
        customer_object=CustomerOptions.objects.get(key='oauthserver')
        oauthserver=customer_object.value
        data={
            'IDP':oauthserver,
            'user':user
        }
        return Response(data=data)

    def post(self,request,pk):
        """
        Initiates SSO for configured IDP.
        """
        user=get_object_or_404(User,pk=pk)
        state=hashlib.md5(str(settings.SECRET_KEY).encode()).hexdigest()
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
        response=redirect(url)
        response["Access-Control-Allow-Origin"]="*"
        response["Access-Control-Allow-Methods"]="GET"
        response.status_code=302
        return response


class GetAccessCodeView(APIView):
    """
    Receive access code from idp.
    """
    renderer_classes=(TemplateHTMLRenderer,)

    def get(self,request):
        """
        Receive code.
        """
        code=request.query_params.get('code')
        state=request.query_params.get('state')
        state_original=hashlib.md5((settings.SECRET_KEY).encode('utf-8')).hexdigest()
        customer_objects=CustomerOptions.objects.get(key='oauthappname')
        oauthapp=customer_objects.value
        oidc_object=Oidcclient.objects.get(application_name=oauthapp)
        data={
            "client_id":oidc_object.client_id,
            "client_secret":oidc_object.client_secret,
            "redirect_uri":oidc_object.redirect_uri,
            "code":code
        }
        token_endpoint=oidc_object.token_endpoint
        if(str(state)==str(state_original)):
            try:
                token_response=requests.post(token_endpoint,data=data)
                token_str=token_response.content.decode('utf-8')
                token_int=token_str.split("=")[1]
                token=token_int.split("&")[0]
            except:
                LOGGER.error('Error while making token request.')
            try:
                enduserinfo_endpoint=oidc_object.enduserinfo_endpoint
                headers={
                    "Authorization":"Bearer "+str(token)
                }
                enduser_res=requests.get(enduserinfo_endpoint,headers=headers)
                enduser=json.loads(enduser_res.content.decode('utf-8'))
            except:
                LOGGER.error('Error while making enduserinfo request.')
            try:
                user_data={
                    "username":enduser['name'],
                    "password":"endusersso",
                    "is_staff":False
                }
                user=User.objects.create(**user_data)
            except:
                LOGGER.error('Error while creating user.')
            tem_data={
                "username":user.username
            }
            return Response(template_name='login/sso_github.html',data=tem_data)
        else:
            LOGGER.error('State received is invalid.')
            return Response(template_name='login/error.html')