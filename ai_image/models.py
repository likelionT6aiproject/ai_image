from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    transformed_image = models.ImageField(upload_to='transformed_images/', null=True, blank=True)
