from django.db import models
from django.contrib.auth.models import User
import cv2


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = cv2.imread(self.image.path, 1)
        if img.shape[0] > 300:
            output_size = (300, 300)
            img = cv2.resize(img, output_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, img)


DAY_CHOICES = (("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"), ("Saturday", "Saturday"), ("Sunday", "Sunday"))
HOURS_CHOICES = (("09:00", "09:00"), ("10:00", "10:00"), ("11:00", "11:00"), ("12:00", "12:00"), ("13:00", "13:00"), ("14:00", "14:00"), ("15:00", "15:00"), ("16:00", "16:00"), ("17:00", "17:00"))
SERVICE_CHOICES = (("Consultation", "Consultation"), ("Healthy Life Plan", "Healthy Life Plan"), ("Diet and Workout", "Diet and Workout"), ("Kinetotherapy", "Kinetotherapy"))


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    Day_Range = models.CharField(max_length=9, choices=DAY_CHOICES, default='Monday', verbose_name="Day")
    Hour = models.CharField(max_length=10, choices=HOURS_CHOICES, default="09:00")
    Service = models.CharField(max_length=17, choices=SERVICE_CHOICES, default='Service1')
    Status = models.CharField(max_length=10, choices=(("pending", "pending"), ("cancelled", "cancelled"), ("confirmed", "confirmed")), default='pending')

    def __str__(self):
        return f'Appointment for {self.user.username} ({self.Day_Range} at {self.Hour})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
