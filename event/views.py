from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import post_event, BlogComment, RegistrationForEvent
from django.shortcuts import HttpResponse, HttpResponseRedirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail



class HomeView(TemplateView):
    template_name = "event/home.html"

def post_list(request):
    post = post_event.objects.all()
    comments = BlogComment.objects.filter(post=post).order_by('-id')
    context = {'post':post,'comments':comments}
    return render(request, 'event/post_event_list.html', context)

def post_detail(request, *args, **kwargs):
    post = get_object_or_404(post_event, pk=kwargs.get("pk"))
    is_registered = False
    if post.register.filter(id=request.user.id).exists():
        is_registered = True

    comments = BlogComment.objects.filter(post=post, reply=None).order_by('-id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = request.POST.get('comment')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = BlogComment.objects.get(id=reply_id)
            comment = BlogComment.objects.create(post=post,user = request.user,comment=comment,reply=comment_qs)
            comment.save()
            messages.success(request,"Your comment has been posted")
            return redirect(request.META.get('HTTP_REFERER')) 
    else:
        comment_form = CommentForm()

    context = {'post': post,
               'is_registered':is_registered,
               'total_registrations':post.total_registrations(),
               'comments':comments,
               'comment_form':comment_form,
              }
    return render(request, 'event/post_event_detail.html', context) 

def event_registration(request, *args, **kwargs):
    post = get_object_or_404(post_event, pk=request.POST.get("post_id"))
    is_registered = False
    if post.register.filter(id=request.user.id).exists():
        post.register.remove(request.user)
        is_registered = False
    else:
        post.register.add(request.user)
        chereg = RegistrationForEvent()
        chereg.event_title = post
        chereg.First_Name = request.user.profile.First_Name
        chereg.Last_Name = request.user.profile.Last_Name
        chereg.Roll_No = request.user.profile.Roll_No
        chereg.School = request.user.profile.School
        chereg.Year = request.user.profile.Year
        chereg.save()
        is_registered = True
        return render(request, 'event/ticket.html', {'chereg' : chereg})
    return redirect(request.META.get('HTTP_REFERER')) 

    #     is_liked = False

    # context = {
    #     'post': post,
    #     # 'is_liked': is_liked,
    #     # 'total_likes': post.total_likes(),
    # }
    # if request.is_ajax():
    #     html = render_to_string('blog/like_section.html', context, request=request)
    #     return JsonResponse({'form': html})

class post_eventCreateView(LoginRequiredMixin, CreateView):
    model = post_event
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class post_eventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post_event
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class post_eventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post_event
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # username = form.cleaned_data.get('username')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')         
    else:
        form = UserRegisterForm()
    return render(request, 'event/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # contact_email = request.user.email
            # send_mail(
            #     'Updated the Profile',
            #     'Your profile has been successfully updated',
            #     'app.info.45@gmail.com',
            #     [contact_email],
            # )
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'event/profile.html', context)

def activate(request, uidb64, token):   
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Your account has been created! You are now able to log in')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

