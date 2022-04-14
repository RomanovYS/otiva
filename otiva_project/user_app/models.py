from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class OtivaUser(AbstractUser):
    """Пользователь сайта"""
    
    USER_TYPES = [
        # Private Owner
        ('PO', 'ЧЛ - Владелец техники'),
        # Private Service
        ('PS', 'ЧЛ - Сервисный инженер'),
        # Company Owner
        ('CO', 'ЮЛ - Владелец техники'),
        # Company Service
        ('CS', 'ЮЛ - Сервисный центр'),
    ]
    
    REQUIRED_FIELDS = ['email']
    
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default='PO',
        
    )
    
    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        verbose_name='Аватар пользователя'
    )

    email = models.EmailField(_('email'), blank=True, unique=True)
    
    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )
    
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )
    
    def is_activation_key_expired(self):
        return now() >= self.activation_key_expires
