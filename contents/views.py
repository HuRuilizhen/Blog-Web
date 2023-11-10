from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from users.models import *


# Create your views here.
@login_required
def personal_blogs(request):
    user = request.user
    blogs = user.blog_set.order_by("date_added")
    context = {"blogs": blogs, "keyword": ""}

    if request.method == "POST":
        context["keyword"] = request.POST.get("keyword")

    return render(request, "personal_blogs.html", context)


def all_blogs(request):
    blogs = Blog.objects.order_by("date_added")
    context = {"blogs": blogs, "keyword": ""}

    if request.method == "POST":
        context["keyword"] = request.POST.get("keyword")

    return render(request, "all_blogs.html", context)


def detail_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = blog.comment_set.order_by("date_added")
    comment_form = CommentForm()
    context = {"blog": blog, "comments": comments, "comment_form": comment_form}
    owner_user = blog.author
    visit_user = request.user
    if owner_user != visit_user:
        profile = owner_user.profile
        profile.visit += 1
        profile.save()
        blog.visit += 1
        blog.save()
    return render(request, "detail_blog.html", context)


@login_required
def add_blog(request):
    if request.method != "POST":
        blogform = BlogForm()
    else:
        blogform = BlogForm(request.POST)
        if blogform.is_valid():
            blog = blogform.save(commit=False)
            blog.author = request.user
            blog.save()
            request.user.profile.number_of_blogs += 1
            request.user.profile.save()
            return HttpResponseRedirect(reverse("contents:all_blogs"))
    context = {"blogform": blogform}
    return render(request, "add_blog.html", context)


@login_required
def edit_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")

    blog = Blog.objects.get(id=blog_id)

    if request.method != "POST":
        blogform = BlogForm(instance=blog)
    else:
        blogform = BlogForm(request.POST, instance=blog)
        if blogform:
            blogform.save()
        return HttpResponseRedirect(reverse("contents:all_blogs"))
    context = {"blog": blog, "blogform": blogform}
    return render(request, "edit_blog.html", context)


@login_required
def hid_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    blog = Blog.objects.get(id=blog_id)
    blog.is_hidden = True
    blog.save()
    return HttpResponseRedirect(reverse("contents:all_blogs"))


@login_required
def display_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    blog = Blog.objects.get(id=blog_id)
    blog.is_hidden = False
    blog.save()
    return HttpResponseRedirect(reverse("contents:all_blogs"))


@login_required
def del_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    Blog.objects.get(id=blog_id).delete()
    user.profile.number_of_blogs -= 1
    user.profile.save()
    return HttpResponseRedirect(reverse("contents:personal_blogs"))


def all_announcements(request):
    announcements = Announcement.objects.order_by("date_added")
    context = {"announcements": announcements}
    return render(request, "all_announcements.html", context)


def detail_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    context = {"announcement": announcement}
    return render(request, "detail_announcement.html", context)


@login_required
def add_announcement(request):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    if request.method != "POST":
        announcementform = AnnouncementForm()
    else:
        announcementform = AnnouncementForm(request.POST)
        if announcementform.is_valid():
            announcement = announcementform.save(commit=False)
            announcementform.author = request.user
            return HttpResponseRedirect(reverse("contents:all_announcements"))
    context = {"announcementform": announcementform}
    return render(request, "add_announcement.html", context)


@login_required
def edit_announcement(request, announcement_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    announcement = Announcement.objects.get(id=announcement_id)

    if request.method != "POST":
        announcementform = AnnouncementForm(instance=announcement)
    else:
        announcementform = AnnouncementForm(
            request.POST, request.FILES, instance=announcement
        )
        if announcementform.is_valid():
            announcementform.save()
        return HttpResponseRedirect(reverse("contents:all_announcements"))
    context = {"announcement": announcement, "announcementform": announcementform}
    return render(request, "edit_announcement.html", context)


@login_required
def del_announcement(request, announcement_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")
    Announcement.objects.get(id=announcement_id).delete()
    return HttpResponseRedirect(reverse("contents:all_announcements"))


@login_required
def add_comment(request, blog_id):
    if request.method != "POST":
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog = Blog.objects.get(id=blog_id)
            comment.save()
        return redirect(f"/detail_blog/{blog_id}/")
    return redirect(f"/detail_blog/{blog_id}/")


@login_required
def del_comment(request, comment_id):
    current_comment = Comment.objects.get(id=comment_id)
    current_blog = current_comment.blog
    comment_user = current_comment.author
    blog_user = current_blog.author
    blog_id = current_blog.id

    if request.user != comment_user and request.user != blog_user:
        raise PermissionDenied("sorry you have no permission")
    Comment.objects.get(id=comment_id).delete()

    return redirect(f"/detail_blog/{blog_id}/")
