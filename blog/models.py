from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#from tinymce.models import HTMLField
import geocoder
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()            # HTMLField() to use tiny
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='post_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    # MUST FIX: ITS NOT SAVING THE PICTURES TO THE FOLDER


# NEW

mapbox_access_token = 'pk.eyJ1IjoibGlvbmZveHByIiwiYSI6ImNrdjV1NWRseTkzb2Yyb2s2NTkyNmswNW4ifQ.UVK1-Mp5uOSx4py0tJqDgg'

class Address(models.Model):
    address = models.CharField(max_length=100)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=mapbox_access_token)
        g = g.latlng  # returns => [lat, long]
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.address