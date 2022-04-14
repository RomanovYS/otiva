import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from user_app.models import OtivaUser


class OtivaUserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = OtivaUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')
    
    def save(self, commit=True):
        user = super().save()
        
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class OtivaUserLoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = OtivaUser
        fields = ('username', 'password')
       
    
        
    