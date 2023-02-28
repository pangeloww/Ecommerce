from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.

#This view return all products
def product_all(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products':products})

#This view returns all product details when a specific item is clicked in the website
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/single.html', {'product':product})

#This is the category list/dropdown menu witch is powered by this view
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'store/category.html', {'category':category, 'products':products})
