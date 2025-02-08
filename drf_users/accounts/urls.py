from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('info/', views.InfoView.as_view(), name='profile'),
    path('latency/', views.LatencyView.as_view(), name='latency'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
