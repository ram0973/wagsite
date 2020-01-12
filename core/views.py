import os
import json
import uuid

from configurations import values
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder
from django.shortcuts import render

from blog.models import Post

POSTS_ON_HOME = 5


def home(request):
    posts = Post.objects.published().order_by('-pub_date')[:POSTS_ON_HOME]
    return render(request, 'core/home.html',
                  {'post_list': posts,
                   'domain': values.Value(environ_name='DOMAIN')})


@login_required
def markdown_uploader(request):
    """
    Markdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if not (request.method == 'POST' and request.is_ajax() or
            ('markdown-image-upload' not in request.FILES)):
        return HttpResponse(_('Invalid request!'))
    image = request.FILES['markdown-image-upload']
    image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg',
                   'image/gif']
    if image.content_type not in image_types:
        data = json.dumps({'status': 405, 'error': _('Bad image format.')},
                          cls=LazyEncoder)
        return HttpResponse(data, content_type='application/json', status=405)
    if image._size > settings.MAX_IMAGE_UPLOAD_SIZE:
        to_mb = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
        data = json.dumps({'status': 405, 'error':
                          _('Maximum image file is %(size) MB.') %
                          {'size': to_mb}}, cls=LazyEncoder)
        return HttpResponse(data, content_type='application/json', status=405)
    img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10],
                                image.name.replace(' ', '-'))
    tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
    def_path = default_storage.save(tmp_file, ContentFile(image.read()))
    img_url = os.path.join(settings.MEDIA_URL, def_path)
    data = json.dumps({'status': 200, 'link': img_url, 'name': image.name})
    return HttpResponse(data, content_type='application/json')
