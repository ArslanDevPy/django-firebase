from django.urls import path
from myapp import views


urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name="home"),
    path('login/', views.LoginTemplateView.as_view(), name="login"),
    path('signup/', views.SignupTemplateView.as_view(), name="signup"),
    path('logout/', views.userLogout, name="logout"),
    path('reset/', views.PasswordResetTemplateView.as_view(), name="reset"),
    path('uploader/', views.UploaderTemplateView.as_view(), name="uploader"),
    path('contact/', views.ContactUS.as_view(), name="contact"),
    path('contact/edit/<uid>/', views.ContactUpdateView.as_view(), name="contact-edit"),
    path('contact/del/<uid>/', views.ContactDeleteView.as_view(), name="contact-delete"),
]
