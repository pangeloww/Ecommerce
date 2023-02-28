import json
import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from basket.basket import Basket
from orders.views import payment_confirmation
from basket.basket import Basket

# Create your views here.
#The view to return that the order has been successfull
#In these views we have the login_Required decorator that requires to be logged in for the func to work
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

#The basket view that returns a total price with all the items in the basket,
#also the sripe key is included to track all the movements made when a order intend is made
@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = 'sk_test_51MNydQIae454BRv064cflrQ5ky9q87umR1gxcTuaDbC76Avz6Fu3qqVyOx7ZbVpx5yvP9wor4MTjqNA1ctv9qOGR00bOHTLezi'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='bgn',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

#The sripe webhook helps to get data thru the csrf token.
#Then the stripe hook passes the information for the order in the
#specific stripe console that can be accesed from the files
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        print('payment confirmation')
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)