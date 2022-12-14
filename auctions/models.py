from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.category}"


class Auctions(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    price = models.DecimalField(max_digits = 12, decimal_places = 2)
    photo = models.URLField()
    category = models.ForeignKey(Categories, on_delete = models.CASCADE, blank = True, null = True)
    seller = models.ForeignKey(User, on_delete = models.CASCADE)
    active = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title}"


class Bids(models.Model):
    amount = models.DecimalField(max_digits = 12, decimal_places = 2)
    bidder = models.ForeignKey(User, on_delete = models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.amount} placed by {self.bidder} on {self.datetime}"


class Comments(models.Model):
    post = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete = models.CASCADE)
    datetime = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user1}: {self.post} on {self.datetime} in {self.auction}"


class Watchlist(models.Model):
    auction = models.ForeignKey(Auctions, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
