from django.urls import path

from . import views

app_name = 'payment'

#The urls for the payment app
urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('webhook', views.stripe_webhook),
]