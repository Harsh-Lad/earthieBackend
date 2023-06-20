from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(null=True, blank=True,max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class HomeSlider(models.Model):
    slideName = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    isMobile = models.BooleanField(default=False)
    slide = models.ImageField(upload_to='slider')

    def __str__(self):
        return self.slideName
    
class HomeBlock(models.Model):
    blockName = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    offerImage = models.ImageField(upload_to='homeBlock')

    def __str__(self):
        return self.blockName

class Categories(models.Model):
    categoryName = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryName
    
class Collections(models.Model):
    collectionName = models.CharField(max_length=255)
    collectionImage = models.ImageField(upload_to='collections')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.collectionName
    

class Products(models.Model):
    productName = models.CharField(max_length=255)
    productDesc = models.TextField()
    productPrice = models.IntegerField()
    product_image = models.ImageField(upload_to='products')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    primary = models.ImageField(upload_to='primary')
    secondary = models.ImageField(upload_to='secondry')
    tertiary = models.ImageField(upload_to='tertiary')
    tags = models.TextField(null=True, blank=True)
    is_in_Offer = models.BooleanField(default=False)
    offerPrice = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    dateUploaded = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collections, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.productName
    


