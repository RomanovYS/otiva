from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
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
    
    user_type = models.CharField(max_length=2, choices=USER_TYPES, default='PO', )
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Аватар пользователя')
    email = models.EmailField(_('email'), blank=True, unique=True)
    activation_key = models.CharField(max_length=128, blank=True, )
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True,)
    
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    
    def is_activation_key_expired(self):
        return now() >= self.activation_key_expires


class Role(models.Model):
    """Роль"""
    
    name = models.CharField(max_length=100, )
    rem = models.CharField(max_length=200, )
    
    def __str__(self):
        return self.name


class Address(models.Model):
    """Адрес пользователя"""
    # user = models.ForeignKey(OtivaUser, on_delete=models.CASCADE, related_name='address')
    area = models.CharField(max_length=100, verbose_name='Регион', null=True)
    country = models.CharField(max_length=100, verbose_name='Страна', null=True, )
    city = models.CharField(max_length=100, verbose_name='Город', null=True, )
    post = models.CharField(max_length=10, null=True, verbose_name='Почтовый индекс', blank=True)
    street = models.CharField(max_length=100, null=True)
    building = models.CharField(max_length=5, verbose_name='Строение', null=True)
    room = models.CharField(max_length=5, verbose_name='Номер квартиры', null=True)
    metro = models.CharField(max_length=50, null=True, blank=True)
    map_link = models.URLField(verbose_name='Ссылка на карту', null=True, blank=True)
    corporate_phone = models.CharField(max_length=15, verbose_name='Корпоративный номер телефона', null=True,
                                       blank=True, default='')
    # url_link =
    office = models.CharField(max_length=5, null=True, verbose_name='Номер офиса', blank=True, default='')
    time = models.CharField(max_length=30, verbose_name='Рабочее время', null=True, blank=True, default='')
    liter = models.CharField(max_length=200, verbose_name='Литeра', null=True, blank=True, default='')
    
    def __str__(self):
        return f'{self.id}, {self.city}, {self.street}, {self.building}'


class Profile(models.Model):
    user = models.OneToOneField(
        OtivaUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
        null=True,
        blank=True,
    )
    
    surname = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
        null=True,
        blank=True,
    )
    
    phone_num = models.CharField(
        max_length=20,
        verbose_name='номер телефона',
        null=True,
        blank=True,
    )
    
    working_position = models.CharField(
        max_length=200,
        verbose_name='Должность',
        null=True,
        blank=True,
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f'Профайл для {self.user.username}'


# signals

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_address(sender, created, instance, **kwargs):
    if created:
        address = Address.objects.create()
        instance.address = address
        instance.save()
