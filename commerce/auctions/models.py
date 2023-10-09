from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self) -> str:
        return f"{self.username}: {self.email}, {self.first_name} {self.last_name}"


class Auction(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auctioneer"
    )
    image = models.ImageField(upload_to="static/images")
    category = models.CharField(max_length=64)
    status = models.CharField(max_length=5)

    def __str__(self) -> str:
        return f"Auction {self.title}: {self.image}{self.description}, category {self.category}, status {self.status} from user {self.user_id}"


class Bids(models.Model):
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="bids"
    )
    starting_bid = models.DecimalField(max_digits=20, decimal_places=10)
    current_bid = models.DecimalField(max_digits=20, decimal_places=10)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self) -> str:
        return f"Auction {self.auction_id}: start {self.starting_bid}, current {self.current_bid}, bidder {self.user_id}"


class Comments(models.Model):
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="comments"
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self) -> str:
        return f'{self.auction_id}: {self.user_id} commented - "{self.comment}"'


class Watchlist(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_favorites"
    )
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="auction_favorite"
    )
