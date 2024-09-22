from django.db import models
import datetime
from django.contrib.auth.models import User #
from django.db.models.signals import post_save #when a user signs up, they use the django authentication system. automatically create a profile



# create Customer Profile
# below inherite (models.Model)
class Profile(models.Model):
	# below models.OneToOneField means that a user can only have 1 account like in FB, youtube etc.
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True , null=True)

	def __str__(self):
		return self.user.username # backend admin section

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		# below Profile is from above class Profile(models.Model):
		user_profile = Profile(user=instance)
		user_profile.save()

#Automate the profile thing
# post_save taken from above import post_save
post_save.connect(create_profile, sender=User) 




#below (models.Model) inherits models
# categories of products
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	# to make category to plural
	class Meta:
		verbose_name_plural = 'categories'

# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

# all of our products
class Product(models.Model):
	name = models.CharField(max_length=100)
	# default = 0 means if no price, it is free. 
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	# below default=1 means if there are no categories, it will just default to the first category 
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	# blank = True means description can be blank. null=True means if it doesnt have a description, no big deal
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')
	# add Sale Stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return self.name

# Customer Orders
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.product
