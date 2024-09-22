from django.shortcuts import render, get_object_or_404
from .cart import Cart
from storeapp.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})



def cart_add(request):
    # Get the cart
    cart = Cart(request) # Cart from cart.py to class Cart():
    # test the POST
    if request.POST.get('action') == 'post': # if were making a post to th`e webpage, its UPPERCASE POST. 
        # Get stuff 
        product_id = int(request.POST.get('product_id')) # ('product_id') taken from product.html to product_id: $('#add-cart').val(),
        product_qty = int(request.POST.get('product_qty'))

        # look up product in DB
        product = get_object_or_404(Product, id=product_id)
        
        # Save to Session
        cart.add(product=product, quantity=product_qty)


        # Get Cart Quantity
        cart_quantity = cart.__len__() # __len__() is taken from cart.py to def __len__(self): 

        # Return response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Product Added to Cart"))
        return response


def cart_delete(request):
    cart = Cart(request)
    # test the POST
    if request.POST.get('action') == 'post': # if were making a post to th`e webpage, its UPPERCASE POST. 
        # Get stuff 
        product_id = int(request.POST.get('product_id')) # ('product_id') taken from product.html to product_id: $('#add-cart').val(),
        # call delete function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, ("Product deleted from Cart"))
        return response
        #return HttpResponse
        #return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    # test the POST
    if request.POST.get('action') == 'post': # if were making a post to th`e webpage, its UPPERCASE POST. 
        # Get stuff 
        #product_id = str(request.POST.get('product_id')) # ('product_id') taken from product.html to product_id: $('#add-cart').val(),
        product_id = int(request.POST.get('product_id')) # ('product_id') taken from product.html to product_id: $('#add-cart').val(),
        product_qty = int(request.POST.get('product_qty'))
        #product_qty = str(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Your CART has been updated"))
        return response
        #return HttpResponse
        #return redirect('cart_summary')














