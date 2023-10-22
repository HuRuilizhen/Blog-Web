from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    re_path("^personal_blogs/$", personal_blogs, name="personal_blogs"),
    re_path("^all_blogs/$", all_blogs, name="all_blogs"),
    re_path("^detail_blog/(?P<blog_id>\d+)/$", detail_blog, name="detail_blog"),
    re_path("^add_blog/$", add_blog, name="add_blog"),
    re_path("^edit_blog/(?P<blog_id>\d+)/$", edit_blog, name="edit_blog"),
    re_path("^hid_blog/(?P<blog_id>\d+)/$", hid_blog, name="hid_blog"),
    re_path("^display_blog/(?P<blog_id>\d+)/$", display_blog, name="display_blog"),
    re_path("^del_blog/(?P<blog_id>\d+)/$", del_blog, name="del_blog"),
    re_path("^add_comment/(?P<blog_id>\d+)/$", add_comment, name="add_comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
