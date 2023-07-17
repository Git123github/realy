from django.urls import path
from advertisements.views import create_ad

urlpatterns = [
    path('', create_ad, name='create_ad'),
    # Другие пути вашего проекта
]
