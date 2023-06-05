from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)

class Listings(models.Model):
    listing_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    isactive = models.BooleanField(default=False)
    current_price = models.DecimalField(max_digits=6,decimal_places=2)
    description = models.TextField()
    title = models.CharField(max_length=20)
    category_choices = [
        ("fashion",'fashion'),
        ("toys",'toys'),
        ("electronics",'electronics'),
        ("home",'home')
    ]
    category = models.CharField(max_length=20,choices=category_choices,default="fashion", blank=True)
    img = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    watchlist = models.ManyToManyField(User, blank=True,null=True,related_name="user")
    last_bidder = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True,related_name="bidder")

    def __str__(self):
        return f"{self.title}"

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    listing_id = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="listing")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user_id}:{self.comment}"

class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bids")
    listing_id = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="bids")
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"{self.price}"


