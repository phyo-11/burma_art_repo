from django.shortcuts import render, redirect
from cart.cart import Cart
from . forms import ShippingForm, PaymentForm
from . models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Product, Profile
import datetime


def orders(request,pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request,"Shipping Status Updated!")
			return redirect('home')

		return render(request, 'payment/orders.html',{'order':order, "items":items})

	else:
		messages.error(request, 'Access Denied!')
		return redirect('home')

def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)

		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']

			# Get the order
			order = Order.objects.filter(id=num)
			# Grab date and time
			now = datetime.datetime.now()
			# Update order
			order.update(shipped=True,date_shipped=now)
			# Redirect 
			messages.success(request,"Shipping Status Updated!")
			return redirect('home')


		return render(request, 'payment/not_shipped_dash.html',{'orders':orders})

		
	else:
		messages.error(request, 'Access Denied!')
		return redirect('home')



def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)

		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']

			# Get the order
			order = Order.objects.filter(id=num)
			# Grab date and time
			now = datetime.datetime.now()
			# Update order
			order.update(shipped=False)
			# Redirect 
			messages.success(request,"Shipping Status Updated!")
			return redirect('home')

		return render(request, 'payment/shipped_dash.html',{'orders':orders})

	else:
		messages.error(request, 'Access Denied!')
		return redirect('home')



def payment_success(request):
	return render(request, 'payment/payment_success.html',{})

def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods()
	totals = cart.cart_total()
	qty = 1 

	if request.user.is_authenticated:
		# Checkout as loggedin user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, 'payment/checkout.html',{'cart_products':cart_products,
		'totals':totals,'qty':qty, 'shipping_form':shipping_form})

	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, 'payment/checkout.html',{'cart_products':cart_products,
		'totals':totals,'qty':qty, 'shipping_form':shipping_form})

def billing_info(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods()
		totals = cart.cart_total()
		qty = 1 

		# Create a session with Shipping Info so other view can use it
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping

		# Check to see if user is logged in
		if request.user.is_authenticated:
			# Get the billing form
			billing_form = PaymentForm()
			return render(request, 'payment/billing_info.html',{'cart_products':cart_products,
		'totals':totals,'qty':qty, 'shipping_info':request.POST, 'billing_form':billing_form})	
		else:
			# Not logged in
			# Get the billing form
			billing_form = PaymentForm()
			return render(request, 'payment/billing_info.html',{'cart_products':cart_products,
		'totals':totals,'qty':qty, 'shipping_info':request.POST, 'billing_form':billing_form})

		shipping_form = request.POST

		return render(request, 'payment/billing_info.html',{'cart_products':cart_products,
		'totals':totals,'qty':qty, 'shipping_form':shipping_form})	
	
	else:
		messages.error(request,"Access Denied.")
		return redirect('home')


def process_order(request):
	if request.method == 'POST':
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods()
		totals = cart.cart_total()
		qty = 1 

		# Get billing info from last page
		payment_form = PaymentForm(request.POST or None)
		# Get shipping session data
		my_shipping = request.session.get('my_shipping')

		# Gather order info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create shipping address from session data
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# Create an order
		if request.user.is_authenticated:
			# Logged in
			user = request.user
			# Create order
			create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
			create_order.save()


			# Add order items
			# Get order id
			order_id = create_order.pk

			# Get product info
			for product in cart_products:
				# Get product id
				product_id = product.id
				# Get product price
				price = product.price
				# Get quantity
				qty = qty
				# Create order item
				create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=qty,price=price)
				create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key ==  "session_key":
					# Delete the key
					del request.session[key]


			# Delete cart from database(old_cart_field in user profile)
			current_user = Profile.objects.filter(user__id=request.user.id)
			current_user.update(old_cart='')

			messages.success(request, 'Order Placed.')
			return redirect('home')

		else:
			# Not logged in
			# Create order
			create_order = Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
			create_order.save()

			# Add order items
			# Get order id
			order_id = create_order.pk

			# Get product info
			for product in cart_products:
				# Get product id
				product_id = product.id
				# Get product price
				price = product.price
				# Get quantity
				qty = qty
				# Create order item
				create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=qty,price=price)
				create_order_item.save()


			# Delete our cart
			for key in list(request.session.keys()):
				if key ==  "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, 'Order Placed.')
			return redirect('home')


		messages.success(request, 'Order Placed.')
		return redirect('home')

	else:
		messages.error(request, 'Access Denied.')
		return redirect('home')