from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.views.generic import CreateView, DetailView, ListView

def home(request):
    return render(request, 'blog_app/home.html')

def about(request):
    return render(request, 'blog_app/about.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/posts.html'
    context_object_name = 'posts' 
    ordering = ['-created_at'] 
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/create_post.html'
    success_url = reverse_lazy('post_list')  # Перенаправление на главную страницу после создания поста
    