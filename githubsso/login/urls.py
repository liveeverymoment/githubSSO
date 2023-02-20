"""
Router path file.
"""
from django.urls import path
from login.views import LoginAPIView

urlpatterns=[
    path('sso/',LoginAPIView.as_view(),name='login_page')
]