from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ("username", "email", 'password1', 'password2')
# clean_email: Ensures that the email is unique when the user registers or updates their profile. 
# It checks if the email already exists in the database and raises a validation error if it does.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","email")
    