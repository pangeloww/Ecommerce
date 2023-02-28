from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail

#The login form of the user.
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'имейл', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'парола',
            'id': 'login-pwd',
        }
    ))

#The user registration form
class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Въведи потребителско име ', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Reqired', error_messages={'required': 'Нужен е имейл'})
    password = forms.CharField(label='Парола', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтори парола', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    #Checks if the username already exists and if so there will be a message and the username field will be cleared form the field
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    #Checks if the password is the same as the password that is required
    #to be typed 2 times and if it is not the same a message will pop up and the password will be cleared form the field
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    #Checks if the email already exists and if so a message will pop up and the email will be cleared form the field
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    #This is the __init__ witch initializates all the attributes for the user we will be working with
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'потребителско име'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'имейл', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'парола'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'повтори парола'})


#This is the form that the user will use to edit his profile
class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'имейл', 'id': 'form-email', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'име', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

#This is the form that the user will use to reset his password.
class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'имейл', 'id': 'form-email'}))

    #Searches for that user and if he doesnt exists a message pops up and email is 
    #cleared form the field, else the password reset process starts
    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'За съжаление не можем да намерим вашия имейл адрес.')
        return email

#This is the confirmation form that the user uses to write his new passwords if the password reset form has been successfull
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'нова парола', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'повтори нова парола', 'id': 'form-new-pass2'}))

