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
    # please add a location field to this
    date = jmodels.jDateField()  # when is the event
    unitl = jmodels.jDateField()  # when singup for the event finishes

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20) # to specify the profession of the user 
                                                 # for instance SysAdmin, Programmer and etc.
    profile_picture = models.ImageField(upload_to='profile_pictures/')

class SubComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=60)

    def __str__(self):
        return self.text

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=60)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subcomments = models.ManyToManyField(SubComment)

    def __str__(self):
        return self.text

    def __str__(self):
        return self.user.first_name

class news(models.Model):
    title=models.CharField(max_length=50,blank=False,null=False)
    text=models.TextField()
    image=models.ImageField(upload_to="image")
    date=jmodels.jDateField()

    def __str__(self):
        return "{}".format(self.title)

   