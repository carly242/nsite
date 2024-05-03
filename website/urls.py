from django.urls import path, include

from .views import *
from .views import connect
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
urlpatterns =[
    
     path('connect/', login_form, name='connect'),
     path('Connected/', connect, name='Connected'),
     path('deconnect/', deconnect, name='deconnect'),
     path('signup/', register_form, name='signup'),
     path('signedup/', registerView, name='signedup'),
     path('oublier_pass/', PasswordResetView.as_view(template_name='dashboard/password_reset_form.html',
        email_template_name='dashboard/password_reset_email.html',
        success_url='/mail_envoye/'
    ), name='oublier_pass' ),
     path('mail_envoye/', PasswordResetDoneView.as_view( template_name='dashboard/password_reset_done.html'
    ), name='mail_envoye'),
     path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html',
        success_url='/password_reset_complete/'
    ), name='confirme_pass'),
     path('pass_effectue/', PasswordResetCompleteView.as_view(template_name='dashboard/password_reset_complete.html'
    ), name='pass_effectue'),

    path('changer_pass/', change_password, name='changer_pass'),
    path('pass_changer', password_change_done, name='pass_changer'),
     
      
    

     
     
     
     
     
     
     
     
      # Publisher URL's
     path('client/', client, name='client'),
     path('menu/', Menu, name='menu'),
     path('trans/', Transport, name='trans'),
     path('finance/', Finance, name='finance'),

     path('', view_profile, name='home'),
     path('profile/edit/', edit_profile, name='edit_profile'),
     path('profile/<slug:slug>/', view_profile_changed, name='profile_changed'),
     path('modifier', login_or_edit_profile, name='modifier'),
      path('building', PageBuilding, name='building'),
     path('fonctionnalite', login_or_functions, name='fonctionnalite'),
     path('checkpass', check_password_for_fonctionnalite, name='checkpass'),
     path('checkmenu', check_password_for_menu, name='checkmenu'),
     path('testify', check_pass, name='testify'),

     
     
     path('aabook_form/', aabook_form, name='aabook_form'),
     path('aabook/', aabook, name='aabook'),
     path('albook/', ABookListView.as_view(), name='albook'),
     path('aepro/<int:pk>', AeditView.as_view(), name='aepro'),
     path('ambook/', AManageBook.as_view(), name='ambook'),
     path('adbook/<int:pk>', ADeleteBook.as_view(), name='adbook'),
     path('aedoc/<int:pk>', AeditDocView.as_view(), name='aedoc'),

    #admin
    path('admin/', dashboard, name='admin'),
    #path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('wluser/', ListUserView.as_view(), name='wluser'),

]


