from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser,RegistrationLog

# Custom User Registration Form

class AppleRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ("email", "password1")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the password2 field
        del self.fields['password2']
        
        
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number


# Custom User Login Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'autofocus': True})
    )


# Custom Set Password Form
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
    )
    