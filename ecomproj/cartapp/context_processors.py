from .cart import Cart

# Create context processor so our cart can work on all pages of the site
def cart(request):
    # Return the default data from our Cart
    return {'cart': Cart(request)} # capital C as in Cart(request) because from import Cart above
