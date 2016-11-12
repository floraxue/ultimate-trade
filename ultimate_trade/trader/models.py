from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # Add link to default User model
    user = models.OneToOneField(User)
    fb_name = models.TextField()
    phone_number = models.TextField()


class Category(models.Model):
	name = models.TextField()
	parent_category = models.ForeignKey("self", 
									    related_name="subcategory",
                               			on_delete=models.CASCADE, 
                               			null=True)
	depth = models.IntegerField()


class SaleItem(models.Model):
	seller = models.ForeignKey(UserProfile, related_name="sale_items",
							   on_delete=models.CASCADE)
	SOLD_STATUS_CHOICES= (
		('sd', 'SOLD'),
		('oh', 'ON HOLD'),
		('av', 'AVAILABLE')
	)
	sold_status = models.CharField(max_length=2, 
								   choices=SOLD_STATUS_CHOICES)
	created_on = models.DateTimeField()
	primary_image = models.ImageField(upload_to='images/user_upload/')
	secondary_image = models.ImageField(upload_to='images/user_upload/')
	optional_image = models.ImageField(upload_to='images/user_upload/', null=True)
	description = models.TextField()
	price = models.DecimalField(max_digits=11, decimal_places=2)
	category = models.ForeignKey(Category, related_name="all_items",
								 on_delete=models.CASCADE)

