from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"
    

class bids(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listings=models.ForeignKey('listings',on_delete=models.CASCADE,  related_name='bid_listings')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
         return f"{self.user}:,{self.user},{self.price}"

class listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.DecimalField(max_digits=10, decimal_places=2 , default=0.00)
    image = models.ImageField(upload_to='auctions/static/auctions/images/' , blank=True, null=True)
    
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, through='watchlist', related_name='watching')
    is_close=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} : {self.description} , {self.bid},{self.image}"

class comments(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        comment = models.CharField(max_length=100)
        listing=models.ForeignKey(listings ,on_delete=models.CASCADE)
        def __str__(self):
             return f"{self.listing}:{self.comment},{self.user}"

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    def __str__(self):
         return f"{self.user}:{self.listing}"
