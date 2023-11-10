from ckeditor.fields import RichTextFormField
from django import forms
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "text_content"]


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "text_content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
