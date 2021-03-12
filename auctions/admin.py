from django.contrib import admin
from .models import User, ListItem, Comment, Bid, WatchlistItem
# Register your models here.

admin.site.register(User)
admin.site.register(ListItem)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchlistItem)