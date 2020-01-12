from django.contrib import admin
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    list_display = ('title', 'image', 'get_markdown_photo_url')


admin.site.register(Photo, PhotoAdmin)
