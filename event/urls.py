"""event_insider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views 
from django.views.generic.base import RedirectView
from .views import post_eventCreateView,post_eventDeleteView,post_eventUpdateView, event_registration
from django.contrib.auth import views as auth_views

admin.site.site_header = "Event Insider Admin"
admin.site.site_header = "Event Insider Admin Panel"
admin.site.index_title = "Welcome to Insider's Pannel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.HomeView.as_view(),name='home'),

    path('post_event/',views.post_list, name = 'post-list'),
    path('post_event/<int:pk>/', views.post_detail, name='post-detail'),

    path('post/new/', post_eventCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', post_eventUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', post_eventDeleteView.as_view(), name='post-delete'),
    path('login/',auth_views.LoginView.as_view(template_name='event/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='event/logout.html'), name='logout'),
 
    path('register/',views.register, name = 'register'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('profile/',views.profile, name = 'profile'),   

    path('',RedirectView.as_view(url="home/")),

]
