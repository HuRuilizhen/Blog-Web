from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    SEX_CHOICES = ((1, "male"), (2, "female"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex_type = models.IntegerField(choices=SEX_CHOICES)
    score = models.IntegerField(default=0)
    number_of_blogs = models.IntegerField(default=0)
    visit = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)
