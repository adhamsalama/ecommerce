from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

class User(AbstractUser):
    pass


class ListItem(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=datetime.now)
    category = models.CharField(max_length=64, blank=True, null=True)
    image_link = models.CharField(max_length=512, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    # auction state, open = True, closed = False
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.owner}"


class Bid(models.Model):
    value = models.FloatField(validators=[MinValueValidator(0)])
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"${self.value} by {self.user} on {self.date}"


class Comment(models.Model):
    text = models.TextField()
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}\n{self.user}  - {self.date}"


class WatchlistItem(models.Model):
    item = models.ForeignKey(ListItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.item.name} - {self.user}"
