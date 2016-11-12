from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    # Add link to default User model
    user = models.OneToOneField(User)
    fb_name = models.CharField()
    phone_number = models.CharField()


class Category(models.Model):
	name = models.CharField()
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
	primary_image = models.ImageField()
	secondary_image = models.ImageField()
	optional_image = models.ImageField(null=True)
	description = models.TextField()
	price = models.IntegerField()
	category = models.ForeignKey(Category, related_name="all_items",
								 on_delete=models.CASCADE)

