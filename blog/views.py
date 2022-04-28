from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Address
from django.views.generic.edit import CreateView

def intro(request):                                 # NEW
    return render(request, 'blog/intro.html')

@login_required
def home(request):
    return render(request, 'blog/home.html')

@login_required
def trending(request):                              # Changed 'About' to 'Trending' tab
    return render(request, 'blog/trending.html')

@login_required
def explore (request):                              # ADDED: 'Explore' tab
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/explore.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/explore.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# NEW

class AddressView(CreateView):
    model = Address
    fields = ['address']
    template_name = 'blog/address.html'
    success_url = '/address/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = 'pk.eyJ1IjoibGlvbmZveHByIiwiYSI6ImNrdjV1NWRseTkzb2Yyb2s2NTkyNmswNW4ifQ.UVK1-Mp5uOSx4py0tJqDgg'
        context['addresses'] = Address.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def AddressDeleteView (request):
    Address.objects.filter(author=request.user).all().delete()
    #Address.objects.all().delete()

    return redirect('profile')
