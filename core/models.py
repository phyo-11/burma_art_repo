from django.db import models
import datetime
from django.contrib.auth.models import User
#Create a user profile by default when user signs up
from django.db.models.signals import post_save


#Create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)  # Fixed incorrect `User` argument
    phone = models.CharField(max_length=15, blank=True)  # Standard length for phone numbers
    address1 = models.CharField(max_length=255, blank=True)  # Longer length for detailed addresses
    address2 = models.CharField(max_length=255, blank=True)  # Optional second address line
    zipcode = models.CharField(max_length=20, blank=True, null=True)  # Global ZIP code lengths
    city = models.CharField(max_length=100, blank=True)  # Reasonable length for city names
    state = models.CharField(max_length=100, blank=True, null=True)  # Optional for countries without states
    country = models.CharField(max_length=100, blank=True)  # Country names typically fit this length
    old_cart = models.CharField(max_length=255, blank=True, null=True)  # Allows more flexibility for data storage

    def __str__(self):
        return self.user.username



#Create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

#Automate the profile
post_save.connect(create_profile,sender=User)


#Categories
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name_plural = 'categories'

#Customers
class Customer(models.Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=100)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

#Products
class Product(models.Model):
    name = models.CharField(max_length=150)  # Increased max_length for longer product names
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Adjusted max_digits for higher price limits
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)  # Changed to TextField for longer descriptions
    image = models.ImageField(upload_to='uploads/product/')
    width = models.DecimalField(max_digits=10, decimal_places=2)  # Increased max_digits for larger dimensions
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # Increased max_digits for heavier products

    def __str__(self):
        return self.name


#Orders
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	address = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)
	

	def __str__(self):
		return self.product


