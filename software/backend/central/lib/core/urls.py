
from django.urls import path
from . import views  # Use relative import


urlpatterns = [
    path('', views.home, name='home'),
 
]
