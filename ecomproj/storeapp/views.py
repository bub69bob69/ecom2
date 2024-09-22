from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
			#SignUpForm is taken from forms.py -> class SignUpForm(UserCreationForm):
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from paymentapp.forms import ShippingForm
from paymentapp.models import ShippingAddress

from django import forms
from django.db.models import Q 
import json #JavaScript Object Notation / kinda like a python dictionary in a Javascript form
# cartapp to cart.py to class Cart():
from cartapp.cart import Cart



def search(request):
	# Determine if they filled out the form
	if request.method == 'POST':
		# below ['searched'] from search.html to name="searched">
		searched = request.POST['searched']
		# Query The Products DB models		icontains search not case sensitive / insensitive example search for python and Python return the same result
									# searches for name from models.py -> class Product(models.Model):
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

		# Tet for null
		if not searched:
			messages.success(request, "The Product doesn't Exist. Try Again Later hehehe")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched': searched})
	else:
		return render(request, "search.html", {})


def update_info(request):
	if request.user.is_authenticated:	# user__id means find the user profile that has user__id of 2 (balut's profile)
		# below Get current user
		current_user = Profile.objects.get(user__id=request.user.id) #at any given time, you can find what user that is by calling the request.user.id 

		# below Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user) #instance=current_user means when they go to the webpage for the first time, it will have their current info already in the form

		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

		if form.is_valid() or shipping_form.is_valid():
			# below Save Original Form
			form.save()
			# below Save Shipping Form
			shipping_form.save()

			# below after updating, login the user again
			#login(request, current_user)
			messages.success(request, "Your Info has been UPDATED")
			return redirect('home')
		#below if they havent filled up the form, they are just going to the page
		return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})

	else:
		messages.success(request, "You must be logged in to Access that Page")
		return redirect('home')


def update_password(request):
	if request.user.is_authenticated: # this means that the user is logged in
		current_user = request.user
		# Did they fill out the form?
		if request.method == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "your password has been updated. please LOG IN agaIN.")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.success(request, error)
					return redirect('update_password')

		else:
			form = ChangePasswordForm(current_user)
			return render(request, 'update_password.html', {'form':form})
	else:
		messages.success(request, "You must be logged inN to view the page")
		return redirect('home')



def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id) #at any given time, you can find what user that is by calling the request.user.id 
		user_form = UpdateUserForm(request.POST or None, instance=current_user) #instance=current_user means when they go to the webpage for the first time, it will have their current info already in the form

		if user_form.is_valid():
			user_form.save()

			# below after updating, login the user again
			login(request, current_user)
			messages.success(request, "User has been UPDATED")
			return redirect('home')
		#below if they havent filled up the form, they are just going to the page
		return render(request, "update_user.html", {'user_form': user_form})

	else:
		messages.success(request, "You must be logged in to Access that Page")
		return redirect('home')

	
def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {'categories':categories})



def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the URL
	try:
		# LOOk up the category. Remember that models.py file it has name = models.CharField(max_length=50)
		category = Category.objects.get(name=foo)
		# category below taken from category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products': products, 'category': category})
	
	except:
		messages.success(request, ('That Category Doesnt work'))
		return redirect('home')


# below choose only one (1) item at a time
def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product': product})


# below displays all the prodcuts
def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products': products})

def about(request):
	return render(request, 'about.html', {})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username'] #['username'] taken from login.html from <input type="text" class="form-control" name="username"
		password = request.POST['password'] #['password'] taken from login.html from <input type="password" class="form-control" name="password"
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			# below "if statement" to check if there is a saved_cart
			if saved_cart:
				# Convert to dictionary using JSON
				# below will convert a string to a python dictionary
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				# key value pairs = {"3":2, "4":6}
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You are currently logged in."))
			return redirect('home')
		else:
			messages.success(request, ("Error, my friend! Kindly try again now or later hehehe"))
			return redirect('login')
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You're logged Out. Try again later aligator hehehe"))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user. below username=username from username = form.cleaned_data['username']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out yor User Info Below"))
			# below send the registered user to the home page
			return redirect('update_info')
		else: # if code above will not be met, the code below will GO DIRECTLY TO THE register page or just show them the page
			messages.success(request, ("A problem occured. Try again please"))
			# below send the registered user to the register page
			return redirect('register')
	else: # below code: if not, show them the page
		# 'form' taken from register.html -> {{ form.as_p }}
		return render(request, 'register.html', {'form': form})