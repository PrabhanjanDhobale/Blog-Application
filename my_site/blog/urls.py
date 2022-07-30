from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('posts', views.AllPostsView.as_view(), name="posts"),
    # path('posts/<slug:slug>', views.hole_post, name="hole_post"),
    path('posts/<slug:slug>', views.SinglePostView.as_view(), name="hole_post"),
    path('read-later', views.ReadLaterView.as_view(), name="read-later")    
]