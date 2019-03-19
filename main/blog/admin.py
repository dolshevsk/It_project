from django.contrib import admin

from .models import Tag, Post

admin.site.register(Post)
admin.site.register(Tag)

