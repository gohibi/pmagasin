from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.html import mark_safe
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True,max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField (User,on_delete=models.CASCADE)
    image =models.ImageField(upload_to="images-users")
    full_name = models.CharField(max_length=200,null=True,blank=True)
    bio = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=200)
    verified =models.BooleanField(default=False)

    def profile_image(self):
        return mark_safe('<img src="%s" width="50" height="50" >' %(self.image.url))

    def __str__(pain):
        return pain.full_name



class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email =  models.CharField(max_length=200)
    phone =  models.CharField(max_length=200)
    subject =  models.CharField(max_length=200)
    message =  models.TextField(max_length=200)

    class Meta:
        verbose_name = "Contact us"
        verbose_name_plural = "Contact us"

    def __str__(self):
        return self.full_name