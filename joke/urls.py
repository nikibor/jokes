from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.JokeListAPIView.as_view(), name='jokes'),
    path('<int:pk>/', views.JokeAPIView.as_view(), name='edit_joke'),
    path('generate/', views.GenerateJokeAPIView.as_view(), name='generate_joke')
]

urlpatterns = format_suffix_patterns(urlpatterns)