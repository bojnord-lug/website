from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Banners(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/image/banners")

    def __str__(self):
        return self.title


class Authors(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to="static/image/authors")
    specialty = models.TextField()
    aboutme = models.TextField()
    facebook = models.CharField(max_length=30, null=True, blank=True)
    twitter = models.CharField(max_length=30, null=True, blank=True)
    youtube = models.CharField(max_length=30, null=True, blank=True)
    instagram = models.CharField(max_length=30, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Event(models.Model):
    title = models.CharField(max_length=30)
    event_type = models.CharField(max_length=100, default="دورهمی", null=True)
    content = models.TextField()
    location = models.TextField()  # where is it
    image = models.ImageField(upload_to="static/image/event")
    presenter = models.ForeignKey(Authors, on_delete=models.CASCADE)
    date = models.DateField()  # when is the event
    time = models.TimeField()  # when singup for the event finishes

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # to specify the profession of the user
    profession = models.CharField(max_length=20)
    # for instance SysAdmin, Programmer and etc.
    profile_picture = models.ImageField(upload_to='profile_pictures/')


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=50, blank=False, null=False)
    text = models.TextField()
    image = models.ImageField(upload_to="static/image")
    date = models.DateField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['date']


class Comment(models.Model):
    author = models.CharField(max_length=60)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False, verbose_name='تایید شده')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class SubComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.CharField(max_length=60)
    text = models.TextField()

    def __str__(self):
        return self.text


class EventImage(models.Model):
    path = models.ImageField(upload_to="static/image/event")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title

    class Meta:
        verbose_name = 'EventImage'
        verbose_name_plural = 'EventImages'


class NewsLetter(models.Model):
    email = models.CharField(max_length=80)
    date = models.DateField()

    class Meta:
        verbose_name = 'NewsLetter'
        verbose_name_plural = 'NewsLetters'
