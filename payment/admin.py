from django.contrib import admin
from . models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an orderitem inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0

# Extend our order model
class OrderAdmin(admin.ModelAdmin):
	model = Order
	readonly_fields = ["date_ordered"]
	fields = ['user','full_name','email','shipping_address','amount_paid','shipped','date_shipped']
	inlines = [OrderItemInline]


# Unregister order model
admin.site.unregister(Order)

# Re-Register order and orderadmin
admin.site.register(Order,OrderAdmin)