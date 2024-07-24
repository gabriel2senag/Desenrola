from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import ChatListView


urlpatterns = [
    path('', views.home, name='home'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('signup/', views.signup, name='signup'),
    path('service_provider_signup/', views.service_provider_signup, name='service_provider_signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('start_chat/<int:provider_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chats/', ChatListView.as_view(), name='chat_list'),



]
