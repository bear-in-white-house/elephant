from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account import views

default_router = DefaultRouter()
default_router.register('register', views.AccountRegisterViewSet, basename='account_register')
default_router.register('login', views.AccountLoginViewSet, basename='account_login')
default_router.register('userInfo', views.AccountInfoViewSet, basename='account_user_info')

urlpatterns = [
    path('getMessageCode', views.GetMsgCode.as_view()),
    path('register', views.GetMsgCode.as_view()),
    path('', include(default_router.urls)),
]