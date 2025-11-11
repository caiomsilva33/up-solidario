from django.contrib import admin
from .models import PointEvent, Badge, UserBadge

admin.site.register(PointEvent)
admin.site.register(Badge)
admin.site.register(UserBadge)