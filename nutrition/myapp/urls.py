from django.urls import path
from . import views
urlpatterns = [
    #path('', views.home)
    path('', views.home),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logout_page, name='logout_page'),
    #path('register/', views.register,name='register'),
    #path('login/login/', views.loginpage )
    #path('logout', views.logout, name='logout')
    path('register/', views.register ),
    path('login/register/', views.register ),
    path('home/home/', views.home ),
    path('contact/', views.contact ),
    path('test/', views.test,name="test" ),
    path('delete/<int:id>/', views.delete_consume,name="delete" ),
    path('bmi/', views.check_bmi,name="bmi" ),
    
    
]