from xml.parsers.expat import model
from django.urls import path
from . import views
from . import models

urlpatterns = [
    path('', views.index, name='index'),
    path('eventsearch',views.eventsearch,name='eventsearch'),
    path('login',views.login,name='login'),
    path('login-m',views.login_m,name='login-m'),
    path('event',views.event,name='event'),
    path('register',views.register,name="register"),
    path('register-m',views.register_m,name="register-m"),
    path('myevent',views.myevent,name='myevent'),
    path('myticket',views.myticket,name='myticket'),
    path('mypage',views.mypage,name='mypage'),
    path('homehost',views.homehost,name='homehost'),
    path('hostevent',views.hostevent,name='hostevent'),
    path('hostnfc',views.hostnfc,name='hostnfc'),
    path('genticket',views.genticket,name='genticket'),
    path('hostnfcget',views.hostnfcget,name="hostnfcget"),
    path('hostnfcget-g',views.hostnfcget_g,name="hostnfcget_g"),
    path('hostnfcget-a',views.hostnfcget_a,name="hostnfcget_a"),
    path('logout',views.logout,name="logout"),
    path('genticket-m',views.genticket_m,name='genticket-m'),
    path('pay-m',views.pay_m,name='pay-m'),
    path('pay',views.pay,name='pay'),
    path('terms',views.terms,name='terms'),
    path('privacy',views.privacy,name='privacy'),
    path('editingmypage', views.editingmypage, name='editingmypage'),
    path('editingmypage-m', views.editingmypage_m, name='editingmypage-m'),
    path('contactUs', views.contactUs, name='contactUs'),
    path('contactUs-m', views.contactUs_m, name='contactUs-m'),
    path('forgotPasswordUse', views.forgotPasswordUse, name='forgotPasswordUse'),
    path('forgotPasswordUse-m', views.forgotPasswordUse_m, name='forgotPasswordUse-m'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    path('forgotPassword-m', views.forgotPassword_m, name='forgotPassword-m'),
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('resetPassword-m', views.resetPassword_m, name='resetPassword-m'),
    path('editMyEvent', views.editMyEvent, name='editMyEvent'),
    path('editMyEvent-m', views.editMyEvent_m, name='editMyEvent-m'),
    path('lp',views.lp,name='lp'),
]