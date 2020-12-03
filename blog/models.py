from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import cv2


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Service(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    content = models.TextField()
    image = models.ImageField(default='consultation.jpg', upload_to='service_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = cv2.imread(self.image.path, 1)
        if img.shape[0] != 300 or img.shape[1] != 200:
            output_size = (300, 200)
            img = cv2.resize(img, output_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, img)