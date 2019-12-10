from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    profession = models.CharField(max_length=20) # to specify the profession of the user 
                                                 # for instance SysAdmin, Programmer and etc.
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)