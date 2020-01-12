from django.db import models
from django.contrib import admin
from martor.widgets import AdminMartorWidget
from .models import Post
from .models import Tag


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
