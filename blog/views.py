from django.shortcuts import render
from blogs.models import Post, Comment

def blog_index(request):
    posts = Post.objects.all().order_by('-created on')
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created on")
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)



def blog_detail(request, pk):
    posts = Post.object.get(pk=pk)
    comments = Comment.objects.filter(posts=posts)
    context = {
        "posts": posts,
        "comments": comments,
    }
    return render(request, "blog/detail.html", context)
