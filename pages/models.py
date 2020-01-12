from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from django import forms


class HomePage(Page):
    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]


class SitePage(Page):
    body = RichTextField(blank=True)
    categories = ParentalManyToManyField('pages.SitePageCategory', blank=True)
    tags = ClusterTaggableManager(through='pages.SitePageTag', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(SitePage, self).get_context(request, *args, **kwargs)
        #context['posts'] = self.posts
        context['site_page'] = self
        context['menu_items'] = self.get_children().filter(live=True, show_in_menus=True)
        return context


@register_snippet
class SitePageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SitePageTag(TaggedItemBase):
    content_object = ParentalKey('SitePage', related_name='site_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
