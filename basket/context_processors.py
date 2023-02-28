from .basket import Basket

#Returns the basket data for the user in a dictionary
def basket(request):
    return {'basket': Basket(request)}