from django.contrib import admin
from .models import Item, Message, Claim


admin.site.register(Item)
admin.site.register(Message)
admin.site.register(Claim)