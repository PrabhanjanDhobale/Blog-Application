from turtle import pos
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
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

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
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
            "comment_form":comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-details.html", context)

# def hole_post(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug) 
#     return render(request, 'blog/post-details.html', {
#         'post': identified_post,
#         "tags": identified_post.tags.all(),
#         "comment_form": CommentForm()
#     })

class ReadLaterView(View):

    def get(self, request):
        stored_post = request.session.get('stored_posts')

        context = {}

        if stored_post is None or len(stored_post) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, 'blog/stored-post.html', context)

    def post(self, request):
        stored_post = request.session.get('stored_posts')

        if stored_post is None:
            stored_post = []

        post_id = int(request.POST['post_id'])
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)

        request.session["stored_posts"] = stored_post

        return HttpResponseRedirect("/")
