from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def index(request):
    products = Product.objects.order_by("updated_at")[:5]
    context = {"featured_products": products}
    return render(request, "store/index.html", context)  # type: ignore


def products(request):
    products = Product.objects.order_by("updated_at")[:5]
    return HttpResponse(products)  # type: ignore


def categories(request):
    return HttpResponse("Hello, world. This is the categories list placeholder")  # type: ignore


def brands(request):
    return HttpResponse("This is the brands list")


def product_detail(request, product_id):
    return HttpResponse("You're looking at the product %s." % product_id)


def auth(request, user_id):
    return HttpResponse("The user is %s" % user_id)


def cart(request, cart_id):
    response = "The cart is %s"
    return HttpResponse(response % cart_id)


def checkout(request):
    return HttpResponse("This is the checkout view")  # type: ignore


def order_confirmation(request):
    return HttpResponse("This is order confirmation")  # type: ignore


def profile(request, user_id):
    return HttpResponse("This is the user %s" % user_id)
