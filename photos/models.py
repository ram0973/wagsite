import datetime
import os
import uuid

from django.db import models
from django.utils.translation import ugettext as _


def get_photo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    path = os.path.join('uploads', 'photos', datetime.datetime.today()
                        .strftime('%Y/%m/%d'))
    os.makedirs(path, mode=0o755, exist_ok=True)
    return os.path.join(path, filename)


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=get_photo_upload_path,
                              blank=True,
                              help_text=_('Photo upload'),
                              verbose_name=_('Photo'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_markdown_photo_url(self):
        return '![{}]({})'.format(self.title, self.image.url)

    get_markdown_photo_url.short_description = 'Markdown photo url'
