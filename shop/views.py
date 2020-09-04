from django.shortcuts import render

from shop.models import Product, Category


def product_in_category(request):
    categories = Category.object.all()
    products = Product.object.all()

    return render(request, 'shop/list.html', {'categories': categories, 'products':products})