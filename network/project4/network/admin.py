from django.contrib import admin
from .models import Posts, User, Follow, Like

admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)

