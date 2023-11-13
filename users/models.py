from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    SEX_CHOICES = ((1, "male"), (2, "female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_photo_url = models.CharField(
        max_length=100,
        default="https://c-ssl.dtstatic.com/uploads/blog/202012/26/20201226211434_62985.thumb.1000_0.jpeg",
    )
    user_description = models.CharField(max_length=200, default="这个人很懒，没有更新过个人描述")
    personal_homepage = RichTextField(config_name="default", default="")
    sex_type = models.IntegerField(choices=SEX_CHOICES)
    score = models.IntegerField(default=0)
    number_of_blogs = models.IntegerField(default=0)
    visit = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)
