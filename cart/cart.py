from core.models import Product, Profile	


class Cart():
	def __init__(self, request):
		self.session = request.session

		# Get request
		self.request = request

		# Get the current session key if it exists
		cart = self.session.get('session_key')

		# If the user is new, no session key! Create one!
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}

		# Make sure cart is available on all pages of site
		self.cart = cart

	def db_add(self, product, quantity):
		product = str(product)
		product_qty = str(quantity)

		# Logic
		if product in self.cart:
			pass
		else:
			self.cart[product] = product_qty


		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'","\"")
			# Save carty to the profile model
			current_user.update(old_cart=str(carty))


	def add(self, product):
		product_id = str(product.id)

		# Logic
		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = 1


		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'","\"")
			# Save carty to the profile model
			current_user.update(old_cart=str(carty))


	def __len__(self):
		return	len(self.cart)


	def get_prods(self):
		# Get ids from cart
		product_ids = self.cart.keys()

		# Use ids to lookup products in database model
		products = Product.objects.filter(id__in=product_ids)

		# Return those looked up products
		return products


	def delete(self, product):
		product_id = str(product)
		#Delete from dictionary/cart
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True

		# Deal with logged in user
		if self.request.user.is_authenticated:
			# Get the current user profile
			current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
			carty = str(self.cart)
			carty = carty.replace("\'","\"")
			# Save carty to the profile model
			current_user.update(old_cart=str(carty))

	def cart_total(self):
		#Get product_ids
		product_ids = self.cart.keys()
		#Lookup those keys in our products database model
		products = Product.objects.filter(id__in=product_ids)
		#Start counting at 0
		total = 0
		#Calculate total price by summing up the prices of all products in the cart
		total = sum(product.price for product in products)
		return total