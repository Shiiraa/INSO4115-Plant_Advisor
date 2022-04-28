from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Profile(models.Model):
    privacy_choices = (
        ("Private", "Private"),
        ("Public", "Public"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics' ,blank=False, null=False)
    bio = models.TextField(default = "None")
    privacy = models.CharField(max_length=9, choices=privacy_choices,default="Public")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)