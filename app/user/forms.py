from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django import forms
from .models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=150, required=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or Email',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username or email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            validate_email(username)
            user = CustomUser.objects.get(email=username)
            if user:
                return user.username
        except Exception as e:
            pass
        return username
    
class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        models= CustomUser
        fields = '__all__'

class ForgotPasswordForm(PasswordResetForm):
    class Meta:
        models = CustomUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email exists in the database
        if not CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is not registered.")
        return email
    
class ResetPasswordForm(SetPasswordForm):
    class Meta:
        models = CustomUser
        fields = '__all__'
    