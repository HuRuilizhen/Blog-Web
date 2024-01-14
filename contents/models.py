from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Label(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    text_content = RichTextField(config_name="default")
    label = models.ManyToManyField(to=Label)
    visit = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_on_personal_page = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    text_content = RichTextField(config_name="default")
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    content = RichTextField(config_name="comment")
    is_hidden = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.content
