from django.db import models
from django.contrib.auth.models import User
from core.models import Product 
#Signal to create a user shipping address by default when user signs up
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=150)  # Adjusted for typical name lengths
    shipping_phone = models.CharField(max_length=15, blank=True)  # Common max length for phone numbers
    shipping_email = models.CharField(max_length=254)  # EmailField automatically validates email format
    shipping_address1 = models.CharField(max_length=255)  # Street addresses can be long
    shipping_address2 = models.CharField(max_length=255, blank=True, null=True)  # Optional second address line
    shipping_zipcode = models.CharField(max_length=20, blank=True, null=True)  # ZIP codes may vary in length and format
    shipping_state = models.CharField(max_length=100, blank=True, null=True)  # States/regions, optional in some cases
    shipping_city = models.CharField(max_length=100)  # City names can vary but are rarely extremely long
    shipping_country = models.CharField(max_length=100)  # Country names typically fit within this length

    # Prevent pluralization
    class Meta:
        verbose_name_plural = "ShippingAddress"

    def __str__(self):
        return f'ShippingAddress - {str(self.id)}'


# Create order model
class Order(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True,null=True)


    # To see it in the admin section
    def __str__(self):
        return f'Order - {str(self.id)}'


#Auto add shipping date
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now

# Create order items model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'



#Create a user shipping address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

#Automate the shipping address
post_save.connect(create_shipping,sender=User)