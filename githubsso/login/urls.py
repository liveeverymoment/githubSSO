"""
Router path file.
"""
from django.urls import path
from login.views import LoginAPIView,GetAccessCodeView

urlpatterns=[
    path('sso/<int:pk>/',LoginAPIView.as_view(),name='login_page'),
    path('getcode/',GetAccessCodeView.as_view(),name='get_access_token')
]