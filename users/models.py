from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfileInfo(models.Model):
    USER = 1
    SUPERVISOR = 2
    MANAGER = 3
    OWNER = 4
    ENGINEER = 5
    TECHNICIAN = 6
    CONTRACTOR = 7
    DEVELOPER = 8
    MARKETING = 9
    SALES = 10
    SOCIAL_MEDIA = 11
    WEB_MONITOR = 12
    HELP_DESK = 13
    SECURITY = 14
    ROLE_CHOICES = (
        (USER, 'User'),
        (SUPERVISOR, 'Supervisor'),
        (MANAGER, 'Manager'),
        (OWNER, 'Owner'),
        (ENGINEER, 'Engineer'),
        (TECHNICIAN, 'Technician'),
        (CONTRACTOR, 'Contractor'),
        (DEVELOPER, 'Developer'),
        (MARKETING, 'Marketing'),
        (SALES, 'Sales'),
        (SOCIAL_MEDIA, 'Social_Media'),
        (WEB_MONITOR, 'Web_Monitor'),
        (HELP_DESK, 'Help_Desk'),
        (SECURITY, 'Security'),
    )
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    state = models.CharField(max_length=10, blank=True)
    zip = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    #defining email an sms alert lists
    alerts_manager = models.BooleanField("alerts_manager",unique=False,null=True,default=False)
    alerts_help_desk = models.BooleanField("alerts_help_desk",unique=False,null=True,default=False)
    alerts_marketing = models.BooleanField("alerts_marketing",unique=False,null=True,default=False)
    alerts_social_media = models.BooleanField("alerts_social_media",unique=False,null=True,default=False)
    alerts_web_monitor = models.BooleanField("alerts_web_monitor",unique=False,null=True,default=False)
    alerts_sales = models.BooleanField("alerts_sales",unique=False,null=True,default=False)
    alerts_developer = models.BooleanField("alerts_developer",unique=False,null=True,default=False)
    alerts_security = models.BooleanField("alerts_security",unique=False,null=True,default=False)
    alerts_accounting = models.BooleanField("alerts_accounting",unique=False,null=True,default=False)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)
    instance.userprofileinfo.save()
     

def __str__(self):
    return self.user.username