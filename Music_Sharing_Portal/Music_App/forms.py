from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Song, ProtectedSong
from django.contrib.auth.models import User
from django.core.validators import validate_email
import re


class SignUpForm(UserCreationForm):
    username = forms.CharField(required='True',
                               label='Username',
                               min_length= 8,
                               max_length= 20,
                               help_text='Required. 8-20 characters. At least 1 uppercase letter, 1 lowercase letter, 1 special character, and 1 number.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email', validators=[validate_email], widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required='True', label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required='True', label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_username(self):
        username = self.cleaned_data['username']

        
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=]).{8,20}$', username):
            raise forms.ValidationError("Username must contain at least 1 uppercase letter, 1 lowercase letter, 1 special character, and 1 number.")

        return username


    def save(self, commit='True'):
        user = super(SignUpForm, self).save(commit='False')
        user.username = self.cleaned_data['username']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']


        if commit:
            user.save()
        return user
    
    
class LoginForm(AuthenticationForm):
    pass


class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('name', 'artist', 'duration', 'mp3_file', 'cover_image')

class ProtectedSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('name', 'artist', 'duration', 'mp3_file', 'cover_image')
    allowed_emails = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        validators=[validate_email],
        help_text='Enter comma-separated email addresses.',
    )
    
    def clean_allowed_emails(self):
        emails = self.cleaned_data['allowed_emails']
        email_list = [email.strip() for email in emails.split(',') if email.strip()]
        for email in email_list:
            validate_email(email)
        return ','.join(email_list)
    
    class Meta:
        model = ProtectedSong
        fields = ['allowed_emails']