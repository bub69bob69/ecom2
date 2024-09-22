from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
# below add to admin area in django back end
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0


# EXtend our Order MODEL
class OrderAdmin(admin.ModelAdmin):
	model = Order 
	# date_ordered from models.py to class Order(models.Model) to date_ordered = models.DateTimeField(auto_now_add=True)
	readonly_fields = ["date_ordered"]
	fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
	#inlines = [OrderItemInLine]
	inlines = [OrderItemInline]

# Unregister Order Model
admin.site.unregister(Order)

#Re-register our Order and OrderAdmin
admin.site.register(Order, OrderAdmin)
