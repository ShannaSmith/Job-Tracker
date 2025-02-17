from os import link
from telnetlib import STATUS
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    networks = models.ManyToManyField(User, related_name='networks', blank=True)
    intro = models.CharField(max_length=250, blank=True)
    title = models.CharField(max_length=100, blank=True)
    hobbies = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"This profile belongs to {self.user.username} with an id of {self.user_id}"

    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(pk=instance.id, user=instance)


# Many to many relationship
class Network_Request(models.Model):
	from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

###############################
#Tuples
###################################
SITES = (
        ('O', 'On-Site'),
        ('R', 'Remote'),
        ('H', 'Hybrid'),
)
STATUS = (
    ('Pending', 'Pending'),
    ('Moving Forward', 'Moving Forward'),
    ('Rejected', 'Rejected'),
)
#######################################################
# Create your models here.
#APPLICATION MODEL
#Note Models
#Photo
#################################################
class Application(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    salary = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=250, blank=True)
    link = models.URLField(max_length=200, blank=True)
    site = models.CharField(
        max_length=1,
        # choices
        choices=SITES,
        default=SITES[0][0]
    )
    status = models.CharField(
        max_length=15,
        # choices
        choices=STATUS,
        default=STATUS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"The application named {self.name} has id of {self.id}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'application_id': self.id})


class Note(models.Model):
    date = models.DateField('note date')
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=250)
    # the foregin key always goes on the many side
    # internally it will be application_id the _id automatically gets added
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def __str__(self):
        return f"note {self.name} on {self.date}"

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for application_id: {self.application_id} @{self.url}"


class Avatar(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for Profile_id: {self.profile_id} @{self.url}"