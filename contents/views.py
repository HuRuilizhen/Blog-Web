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
    
    if (request.method == "POST"):
        context["keyword"] = request.POST.get("keyword")
    
    return render(request, "personal_blogs.html", context)


def all_blogs(request):
    blogs = Blog.objects.order_by("date_added")
    context = {"blogs": blogs, "keyword": ""}
    
    if (request.method == "POST"):
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
        new_title = "edit title here"
        new_content = "edit content here"
    else:
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        composer = request.user
        Blog.objects.create(title=new_title, text_content=new_content, author=composer)
        return HttpResponseRedirect(reverse("contents:all_blogs"))
    context = {"new_title": new_title, "new_content": new_content}
    return render(request, "add_blog.html", context)


@login_required
def edit_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")

    blog = Blog.objects.get(id=blog_id)

    if request.method != "POST":
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("contents:all_blogs"))
    context = {"form": form, "blog": blog}
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
    user= Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    Blog.objects.get(id=blog_id).delete()
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
    if request.method != "POST":
        new_title = "edit title here"
        new_content = "edit content here"
    else:
        new_title = request.POST.get("title")
        new_content = request.POST.get("content")
        composer = request.user
        Announcement.objects.create(
            title=new_title, text_content=new_content, author=composer)
        return HttpResponseRedirect(reverse("contents:all_announcements"))
    context = {"new_title": new_title, "new_content": new_content}
    return render(request, "add_announcement.html", context)


@login_required
def edit_announcement(request, announcement_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    announcement = Announcement.objects.get(id=announcement_id)

    if request.method != "POST":
        form = AnnouncementForm(instance=announcement)
    else:
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("contents:all_announcements"))
    context = {"form": form, "announcement": announcement}
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
