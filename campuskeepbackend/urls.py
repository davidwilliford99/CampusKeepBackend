"""
URL configuration for campuskeepbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from campuskeepbackend import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('users/login/', views.loginUser),
    path('users/info/', views.userInfo),
    path('getUsername/', views.getUsername),

    path('items/', views.item_list),
    path('itemsByCategory/', views.items_by_category),
    path('itemsByFinder/', views.items_by_finder),

    path('getMessages/', views.getMessages),
    path('newMessage/', views.newMessage),
    path('getConversation/', views.getConversation),
    path('getConversationList/', views.getConversationList),

    path('claims/', views.claim_list),
    path('verifyClaim/', views.verifyClaim),
    path('denyClaim/', views.denyClaim),
    
]
