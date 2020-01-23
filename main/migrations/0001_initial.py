# Generated by Django 2.2.8 on 2020-01-20 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hitcount.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('image', models.ImageField(upload_to='static/image/authors')),
                ('specialty', models.TextField()),
                ('aboutme', models.TextField()),
                ('facebook', models.CharField(blank=True, max_length=30, null=True)),
                ('twitter', models.CharField(blank=True, max_length=30, null=True)),
                ('youtube', models.CharField(blank=True, max_length=30, null=True)),
                ('instagram', models.CharField(blank=True, max_length=30, null=True)),
                ('website', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='static/image/banners')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('location', models.TextField()),
                ('image', models.ImageField(upload_to='static/image/event')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('presenter', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='main.Authors')),
                ('event_type', models.CharField(
                    max_length=100, default="دورهمی", null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubComment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=60)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=20)),
                ('profile_picture', models.ImageField(
                    upload_to='profile_pictures/')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('image', models.ImageField(upload_to='static/image')),
                ('date', models.DateField()),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='main.Authors')),
                ('category', models.ManyToManyField(to='main.Category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['date'],
            },
            bases=(models.Model, hitcount.models.HitCountMixin),
        ),
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ImageField(upload_to='static/image/event')),
                ('event', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='main.Event')),

            ],
            options={
                'verbose_name': 'EventImage',
                'verbose_name_plural': 'EventImages',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=60)),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('post', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='main.Post')),
                ('subcomments', models.ManyToManyField(to='main.SubComment')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
