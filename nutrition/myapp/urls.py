from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #path('', views.home)
    path('/', views.home),
    path('login/', views.loginpage, name='login'),
    path('login/login/', views.loginpage, name='login'),
    path('logout/', views.logout_page, name='logout_page'),
   
    path('register/', views.register ),
    path('login/register/', views.register ),
    path('home/home/', views.home ),
    #path('contact/', views.contact ),
    path("contact/", views.contact, name="contact"),
    path('test/contact/', views.contact, name="contact"),    
    path('test/', views.test,name="test" ),
    path('login/test/', views.test,name="test" ),
    path('delete/<int:id>/', views.delete_consume,name="delete"),
    path('bmi/', views.check_bmi,name="bmi" ),
    path("password_reset/", views.password_reset_request,name="password_reset"),
    path("login/password_reset/", views.password_reset_request,name="password_reset"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="myapp/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'), name='password_reset_complete'),      

]