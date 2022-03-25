"""HANKEN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('#################', admin.site.urls),
    path('', include('hanken2.urls')),
    path('login', include('hanken2.urls')),
    path('login-m', include('hanken2.urls')),
    path('eventsearch', include('hanken2.urls')),
    path('event',include('hanken2.urls')),
    path('register',include('hanken2.urls')),
    path('register-m',include('hanken2.urls')),
    path('myevent',include('hanken2.urls')),
    path('myticket',include('hanken2.urls')),
    path('mypage',include('hanken2.urls')),
    path('homehost',include('hanken2.urls')),
    path('hostevent',include('hanken2.urls')),
    path('hostnfc',include('hanken2.urls')),
    path('genticket',include('hanken2.urls')),
    path('hostnfcget',include('hanken2.urls')),
    path('hostnfcget-g',include('hanken2.urls')),
    path('hostnfcget-a',include('hanken2.urls')),
    path('logout',include('hanken2.urls')),
    path('genticket-m',include('hanken2.urls')),
    path('pay',include('hanken2.urls')),
    path('pay-m',include('hanken2.urls')),
    path('terms',include('hanken2.urls')),
    path('privacy',include('hanken2.urls')),
    path('editingmypage',include('hanken2.urls')),
    path('editingmypage-m',include('hanken2.urls')),
    path('contactUs',include('hanken2.urls')),
    path('contactUs-m',include('hanken2.urls')),
    path('forgotPasswordUse',include('hanken2.urls')),
    path('forgotPasswordUse-m',include('hanken2.urls')),
    path('forgotPassword',include('hanken2.urls')),
    path('forgotPassword-m',include('hanken2.urls')),
    path('resetPassword',include('hanken2.urls')),
    path('resetPassword-m',include('hanken2.urls')),
    path('editMyEvent',include('hanken2.urls')),
    path('editMyEvent-m',include('hanken2.urls')),
    path('lp',include('hanken2.urls')),
]