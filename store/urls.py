from django.urls import path
from . import views

app_name = 'store'

#All urls for the store app
urlpatterns = [
    path('', views.product_all, name='store_home'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]