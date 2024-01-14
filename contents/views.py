from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from .forms import *
from users.models import *
from users.views import user_home_view
from Blogs.settings import BLOGS_PER_PAGE


# Create your views here.
def blog_user_home_view(request, blog_id):
    user_id = Blog.objects.get(id=blog_id).author.id
    return user_home_view(request, user_id)


def comment_user_home_view(request, comment_id):
    user_id = Comment.objects.get(id=comment_id).author.id
    return user_home_view(request, user_id)


def announcement_user_home_view(request, announcement_id):
    user_id = Announcement.objects.get(id=announcement_id).author.id
    return user_home_view(request, user_id)


@login_required
def personal_blogs(request):
    user = request.user
    blogs = user.blog_set.filter(is_delete=False)

    keyword = request.GET.get("keyword")
    if keyword:
        print(keyword)
        blogs = blogs.filter(title__contains=keyword)
    else:
        keyword = ""

    blogs = blogs.order_by("-date_added")

    pages = Paginator(blogs, BLOGS_PER_PAGE)
    pagenum = request.GET.get("pagenum")

    try:
        pagenum = int(pagenum)
    except Exception:
        pagenum = 1

    if pagenum not in pages.page_range:
        pagenum = 1

    pagelist = pages.page_range[
        max(pagenum - 3, 1) - 1 : min(pages.num_pages, pagenum + 3)
    ]

    blogs = pages.page(pagenum)
    context = {
        "blogs": blogs,
        "keyword": keyword,
        "pagenum": pagenum,
        "pagelist": pagelist,
    }

    return render(request, "personal_blogs.html", context)


def all_blogs(request):
    blogs = Blog.objects.filter(
        is_delete=False,
        is_hidden=False,
    )

    author = request.GET.get("author")
    if author:
        blogs = blogs.filter(author__username__contains=author)
    else:
        author = ""

    keyword = request.GET.get("keyword")
    if keyword:
        blogs = blogs.filter(
            Q(title__contains=keyword) | Q(author__username__contains=keyword)
        )
    else:
        keyword = ""

    blogs = blogs.order_by("-date_added")

    pages = Paginator(blogs, BLOGS_PER_PAGE)
    pagenum = request.GET.get("pagenum")
    try:
        pagenum = int(pagenum)
    except Exception:
        pagenum = 1
    if pagenum not in pages.page_range:
        pagenum = 1
    pagelist = pages.page_range[
        max(pagenum - 3, 1) - 1 : min(pages.num_pages, pagenum + 3)
    ]

    blogs = pages.page(pagenum)
    context = {
        "blogs": blogs,
        "keyword": keyword,
        "author": author,
        "pagenum": pagenum,
        "pagelist": pagelist,
    }

    return render(request, "all_blogs.html", context)


def detail_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    owner_user = blog.author
    visit_user = request.user

    if owner_user != visit_user and blog.is_hidden:
        raise PermissionDenied("sorry you have no permission")

    comments = blog.comment_set.filter(is_delete=False).order_by("date_added")
    commentform = CommentForm()
    context = {"blog": blog, "comments": comments, "commentform": commentform}

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
def hid_blog_on_personal_page(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    blog = Blog.objects.get(id=blog_id)
    blog.is_on_personal_page = False
    blog.save()
    return user_home_view(request, user_id=user.id)


@login_required
def display_blog_on_personal_page(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")
    blog = Blog.objects.get(id=blog_id)
    blog.is_on_personal_page = True
    blog.save()
    return user_home_view(request, user_id=user.id)


@login_required
def del_blog(request, blog_id):
    user = Blog.objects.get(id=blog_id).author
    if request.user != user:
        raise PermissionDenied("sorry you have no permission")

    blog = Blog.objects.get(id=blog_id)
    blog.is_delete = True
    blog.save()

    user.profile.number_of_blogs -= 1
    user.profile.save()

    return HttpResponseRedirect(reverse("contents:personal_blogs"))


def all_announcements(request):
    announcements = Announcement.objects.filter(is_delete=False).order_by("-date_added")
    context = {"announcements": announcements}
    return render(request, "all_announcements.html", context)


def detail_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)

    if announcement.is_delete == True:
        raise PermissionDenied("sorry you have no permission")

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
            announcement.author = request.user
            announcement.save()
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

    announcement = Announcement.objects.get(id=announcement_id)
    announcement.is_delete = True
    announcement.save()

    return HttpResponseRedirect(reverse("contents:all_announcements"))


@login_required
def add_comment(request, blog_id):
    if request.method != "POST":
        commentform = CommentForm()
    else:
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
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

    comment = Comment.objects.get(id=comment_id)
    comment.is_delete = True
    comment.save()

    return redirect(f"/detail_blog/{blog_id}/")


@login_required
def update_user_number_of_blogs(request):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")
    users = User.objects.all()
    for user in users:
        user.profile.number_of_blogs = Blog.objects.filter(author=user).count()
        user.profile.save()
    return HttpResponseRedirect(reverse("users:ranklist"))


@login_required
def recover_all_user_blogs(request):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    blogs = Blog.objects.filter(is_delete=True)
    for blog in blogs:
        blog.is_delete = False
        blog.save()
        blog.author.profile.number_of_blogs += 1
        blog.author.profile.save()

    return HttpResponseRedirect(reverse("contents:all_blogs"))


@login_required
def recover_user_blogs(request, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    owner_user = User.objects.get(id=user_id)

    blogs = Blog.objects.filter(is_delete=True, author=owner_user)
    for blog in blogs:
        blog.is_delete = False
        blog.save()
        owner_user.profile.number_of_blogs += 1
        owner_user.profile.save()

    return HttpResponseRedirect(reverse("contents:all_blogs"))


@login_required
def recover_blog(request, blog_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    blog = Blog.objects.get(id=blog_id)
    owner_user = blog.author

    blog.is_delete = False
    blog.save()

    owner_user.profile.number_of_blogs += 1
    owner_user.profile.save()

    return HttpResponseRedirect(reverse("contents:all_blogs"))


@login_required
def recover_blog_comment(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if not (request.user.is_superuser or request.user != blog.author):
        raise PermissionDenied("sorry you have no permission")

    comments = blog.comment_set.filter(is_delete=True)
    for comment in comments:
        comment.is_delete = False
        comment.save()

    return HttpResponseRedirect(reverse("contents:detail_blog", args=(blog_id,)))


@login_required
def recover_comment(request, comment_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    comment = Comment.objects.get(id=comment_id)
    comment.is_delete = False
    comment.save()

    blog_id = comment.blog.id

    return HttpResponseRedirect(reverse("contents:detail_blog", args=(blog_id,)))


@login_required
def recover_all_announcements(request):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    announcements = Announcement.objects.filter(is_delete=True)
    for announcement in announcements:
        announcement.is_delete = False
        announcement.save()

    return HttpResponseRedirect(reverse("contents:all_announcements"))


@login_required
def recover_announcement(request, announcement_id):
    if not request.user.is_superuser:
        raise PermissionDenied("sorry you have no permission")

    announcement = Announcement.objects.get(id=announcement_id)
    announcement.is_delete = False
    announcement.save()

    return HttpResponseRedirect(reverse("contents:all_announcements"))
