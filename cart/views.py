from django.shortcuts import render, get_object_or_404
from . cart import Cart
from core.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods()
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products,'totals':totals})

def cart_add(request):
	#Get the cart
	cart = Cart(request)

	#test for POST
	if request.POST.get('action') == 'post':

		#Get stuff
		product_id = int(request.POST.get('product_id'))

		#Lookup	product in DB
		product = get_object_or_404(Product, id=product_id)

		#Save to session
		cart.add(product=product)
		#Get Cart Quantity
		cart_quantity = cart.__len__()

		#Return response
		#response = JsonResponse({'Product Name':product.name})
		response = JsonResponse({'qty':cart_quantity})
		messages.success(request,('Product is added to the shopping cart!'))
		return response


def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		#Get stuff
		product_id = int(request.POST.get('product_id'))
		#Call  delete function in Cart
		cart.delete(product=product_id)

	response = JsonResponse({'product':product_id})
	messages.error(request,('Product is removed from the shopping cart!'))
	#return redirect('cart_summary')
	return response

def cart_update(request):
	pass