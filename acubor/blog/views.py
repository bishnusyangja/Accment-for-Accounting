from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Blog
from blog.forms import BlogForm


try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


def list_blog_entries(request):
    objs = Blog.objects.all()
    return render(request, 'list_blog_entries.html', {'objs': objs})


def view_blog_entry(request, id):
    obj = get_object_or_404(Blog, id=id)
    return render(request, 'view_blog_entry.html', {'obj': obj})


def view_blogs_by_author(request, username):
    user = User.objects.get(username=username)
    objs = Blog.objects.filter(author=user)
    return render(request, 'view_blogs_by_author.html', {'objs': objs, 'user': user})


@login_required
def blog_entry_form(request, id=None):
    if id:
        obj = get_object_or_404(Blog, id=id, author=request.user)
        scenario = 'Update'
    else:
        obj = Blog()
        scenario = 'Create'
    if request.POST:
        form = BlogForm(data=request.POST, instance=obj)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect(reverse('list_blog_entries'))
    else:
        form = BlogForm(instance=obj)
    return render(request, 'blog_form.html', {
        'scenario': scenario,
        'form': form,
    })


@login_required
def delete_blog_entry(request, id):
    obj = get_object_or_404(Blog, id=id, author=request.user)
    obj.delete()
    return redirect(reverse('list_blog_entries'))