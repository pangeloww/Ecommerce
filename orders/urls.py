from django.urls import path
from . import views

app_name = 'orders'

#The url pattern to the add func of the orders app
urlpatterns = [
    path('add/', views.add, name='add'),
]