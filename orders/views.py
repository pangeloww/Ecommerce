from django.shortcuts import render
from django.http.response import JsonResponse
from basket.basket import Basket
from .models import Order, OrderItem

# Create your views here.

#The add view for the order
def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2',city='city',phone='phone',post_code='postcode', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response

#Order confirmation view
#Трябва да го оправя
def payment_confirmation(data):
    print('payment confirm')
    Order.objects.filter(order_key=data).update(billing_status=True)

#Returns the user order. Gets the user id and works with it
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders

