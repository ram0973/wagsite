# Generated by Django 2.1.7 on 2019-03-04 10:20

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Post image', upload_to=blog.models.get_image_upload_path, verbose_name='Post image')),
                ('title', models.CharField(help_text='255 characters', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(help_text='Post slug, unique for post date', unique_for_date='pub_date', verbose_name='Slug')),
                ('html_excerpt', models.TextField(blank=True, editable=False)),
                ('html_content', models.TextField(blank=True, editable=False)),
                ('markdown_content', models.TextField(verbose_name='Post full text')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publication date')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
                ('hits', models.IntegerField(default=0, editable=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='all', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='255 symbols max', max_length=255, verbose_name='Tag name')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='all', to='blog.Tag', verbose_name='Tags'),
        ),
    ]
