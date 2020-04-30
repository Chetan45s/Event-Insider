from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, BlogComment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text = 'Required')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['First_Name','Last_Name','School','Roll_No','Year','club_joined','image',]


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=2000, label="", widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here', 'rows':'4','cols':'50'}))
    class Meta:
        model = BlogComment
        fields = ('comment',)