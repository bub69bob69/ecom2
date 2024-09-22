from storeapp.models import Product, Profile



class Cart():
    def __init__(self, request):
        self.session = request.session
        # get request
        self.request = request

        # Get the current session key if it exists
        # if the 'session_key' is not found, they're a new user
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        
        # Make sure cart is available on all pages of site
        self.cart = cart
        # above to make sure this works on every page of our site, we need a context processor
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic. below have you added them to the cart? no need to add it again
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        # below save the cart.
        self.session.modified = True

        # Deal wuth logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile         self.request.user.id is the logged in user 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            # Update old_cart from storeapp to models to class Profile(models.Model):
            current_user.update(old_cart=str(carty))




    # add anything to the cart, the function below will do
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic. below have you added them to the cart? no need to add it again
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            # below add it to the cart
            self.cart[product_id] = int(product_qty)

        # below save the cart.
        self.session.modified = True

        # Deal wuth logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile         self.request.user.id is the logged in user 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            # Update old_cart from storeapp to models to class Profile(models.Model):
            current_user.update(old_cart=str(carty))



    def cart_total(self):
        # Get product IDs
        product_ids = self.cart.keys()
        # look up those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities 
        quantities = self.cart
        # Starting counting at 0 (zero)
        total = 0

        # below, loop through the items of our cart and add everythin up 
        # for key and value '2':5 ,'4':1,
        for key, value in quantities.items():
            # Convert key string into int (integer) so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)


        return total


    # below create a filter that will get the lenght
    def __len__(self):
        return len(self.cart) # len() is a function that will count the lenght in the cart
    
    # below code is to see whats inside the cart
    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys() # why keys? - add the id of the product. go to product.html, the button grabs the product id <button type="button" value="{{ product.id }}" and goes to product_id: $('#add-cart').val(), and posted to our card_add view url: '{% url 'cart_add' %}'. if we go to views.py, that id is added cart.add(product=product)

        #Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        # return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #product_qty = str(quantity)

        # Get the cart
        ourcart = self.cart
        #Update Dictionary/cart. pass in the product_id
        ourcart[product_id] = product_qty
        # below what does this mean?
        self.session.modified = True

        
        # Deal wuth logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile         self.request.user.id is the logged in user 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            # Update old_cart from storeapp to models to class Profile(models.Model):
            current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart

        if product_id in self.cart:
            # below says delele product(s) from cart
            del self.cart[product_id]

        # save our session after weve modified it. to let the program know we modified this
        self.session.modified = True

        # Deal wuth logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile         self.request.user.id is the logged in user 
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            # Update old_cart from storeapp to models to class Profile(models.Model):
            current_user.update(old_cart=str(carty))



