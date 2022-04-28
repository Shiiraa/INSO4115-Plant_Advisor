from django.urls import path
from django.contrib import admin
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.intro, name="blog-intro"),                   # CHANGED INTRO PAGE
    path('trending/', views.trending, name='blog-trending'),    # CHANGED 'About' to 'Trending'
    path('explore/', views.explore, name='blog-explore'),       # NEW
    path('home/', views.home, name='blog-home'),
    # NEW
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    #NEW (for the map)
    path('address/', AddressView.as_view(), name='blog-address'),
    path('address/delete/', views.AddressDeleteView, name='delete-address')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)