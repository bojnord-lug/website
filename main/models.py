from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


class PostImage(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField()

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    location = models.TextField()  # where is it
    image = models.ImageField(upload_to="static/image/")
    presenter = models.TextField(default="not specified")
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


class SubComment(models.Model):
    author = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.text


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    text = models.TextField()
    image = models.ImageField(upload_to="static/image")
    date = models.DateField()
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, null=True)
    author = models.CharField(
        max_length=50, blank=False, null=False, default="not specified")
    tags = models.TextField(default="not specified")

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['date']


class Comment(models.Model):
    author = models.CharField(max_length=60)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subcomments = models.ManyToManyField(SubComment)

    def __str__(self):
        return self.text

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Authors(models.Model):
    name = models.CharField(max_length=60)
    specialty = models.TextField()
    facebook = models.TextField()
    twitter = models.TextField()
    youtube = models.TextField()
    instagram = models.TextField()
    website = models.TextField()

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
