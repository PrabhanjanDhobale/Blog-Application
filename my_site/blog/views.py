from turtle import pos
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
class Index(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"

class SinglePostView(DetailView):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm()
        }
        return render(request, "blog/post-details.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            
            return HttpResponseRedirect(reverse("hole_post", args=[slug]))

        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form
        }
        return render(request, "blog/post-details.html", context)

# def hole_post(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug) 
#     return render(request, 'blog/post-details.html', {
#         'post': identified_post,
#         "tags": identified_post.tags.all(),
#         "comment_form": CommentForm()
#     })

