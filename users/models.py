from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField

# Create your models here.
class UserProfileInfo(models.Model):
    USER = 1
    SUPERVISOR = 2
    MANAGER = 3
    ROLE_CHOICES = (
        (USER, 'User'),
        (SUPERVISOR, 'Supervisor'),
        (MANAGER, 'Manager'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=10, blank=True)
    zip = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)
    instance.userprofileinfo.save()
    
    
    
    
    
    
    
    
     

def __str__(self):
    return self.user.username