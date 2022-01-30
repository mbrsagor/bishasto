from django.urls import path
from user import views

urlpatterns = [
    path('registration/', views.UserCreateAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('profile/', views.ProfileAPIView.as_view()),
    path('profile/<pk>/', views.ProfileUpdateView.as_view()),
]
