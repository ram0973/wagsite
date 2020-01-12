from django.views import generic
from django.views.generic import DateDetailView

from .models import Post


class PostListView(generic.ListView):
    queryset = Post.objects.published()
    allow_future = False
    paginate_by = 5


class PostDateDetailView(DateDetailView):
    queryset = Post.objects.published()
    date_field = 'pub_date'
    allow_future = False
    month_format = '%m'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        self.object.add_hits()
        return self.render_to_response(context)
