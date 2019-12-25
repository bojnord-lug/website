from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20) # to specify the profession of the user 
                                                 # for instance SysAdmin, Programmer and etc.
    profile_picture = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return self.user.first_name

class news(models.Model):
    title=models.CharField(max_length=50,blank=False)
    text=models.TextField()
    image=models.ImageField(upload_to="image")
    date=models.DateField()

    def __str__(self):
        return "{}".format(self.title)

   