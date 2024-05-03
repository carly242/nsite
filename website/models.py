from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .managers import CustomUserManager
from django.utils.text import slugify


#User = get_user_model()


#class pour les utilisateurs 
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, default="your name")
    function = models.CharField(max_length=100, null=True, default="your name")
    email = models.CharField(max_length=100, null=True, default="email")
    email_bureau = models.CharField(max_length=100, null=True, default="office number")
    city = models.CharField(max_length=100, null=True, default="adress")
    phone_number = models.CharField(max_length=100, null=True, default="your name")
    office_number = models.CharField(max_length=100, null=True, default="office mail")
    website = models.CharField(max_length=500, blank=True, null=True, default="website")
    
    
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Générer le slug à partir du nom d'utilisateur
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.name



def get_current_user(request):
    return get_user(request)

#class pour les documents
class Document(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='website/PDF/')