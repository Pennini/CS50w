from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self) -> str:
        return f"User {self.id}: {self.username}"


class Auction(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=128)
    description = models.TextField()
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auctioneer"
    )
    image = models.ImageField(upload_to="images/", blank=True)
    category = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='open')

    def __str__(self) -> str:
        return f"Auction {self.id}: {self.title}"


class Bids(models.Model):
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="bids"
    )
    starting_bid = models.DecimalField(max_digits=20, decimal_places=10)
    current_bid = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", blank=True, null=True)

    def __str__(self) -> str:
        return f"Auction {self.auction_id}"


class Comments(models.Model):
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="comments"
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f'Auction {self.auction_id}: {self.user_id}'


class Watchlist(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_favorites"
    )
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auction_favorite"
    )
