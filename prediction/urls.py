from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
]
