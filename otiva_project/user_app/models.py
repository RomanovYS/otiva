from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
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
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    
    def is_activation_key_expired(self):
        return now() >= self.activation_key_expires


class Role(models.Model):
    """Роль"""
    
    name = models.CharField(max_length=100, )
    rem = models.CharField(max_length=200, )
    
    def __str__(self):
        return self.name


class Country(models.Model):
    """Страна производитель"""
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Страна изготовитель')
    short_name = models.CharField(max_length=50, unique=True, verbose_name='Краткое обозначение страны')
    present = models.BooleanField(verbose_name='Существует кампания', default=True, )
    
    def __str__(self):
        return self.name


class Area(models.Model):
    """Область"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Название региона')
    
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name='Принадлежность региона')
    
    def __str__(self):
        return self.name


class City(models.Model):
    """Город"""
    
    name = models.CharField(max_length=50, )
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, )
    remark = models.CharField(max_length=200, verbose_name='Дополнение')
    
    def __str__(self):
        return self.name


class Postcode(models.Model):
    """Индекс"""
    
    post_code = models.CharField(max_length=6, )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, )
    
    city = models.ForeignKey(City, on_delete=models.CASCADE, )
    
    def __str__(self):
        return self.post_code


class Street(models.Model):
    name = models.CharField(max_length=100, )
    
    def __str__(self):
        return self.name


class MetroLine(models.Model):
    """Ветка метро"""
    
    name = models.CharField(max_length=100, verbose_name='Название ветки метро')
    color = models.CharField(max_length=50, verbose_name='Цвет ветки метро')
    city = models.ForeignKey(City, on_delete=models.CASCADE, )
    
    def __str__(self):
        return self.name


class Metro(models.Model):
    """Метро"""
    name = models.CharField(max_length=50, )
    city = models.ForeignKey(City, on_delete=models.CASCADE, )
    metro_line = models.ForeignKey(MetroLine, on_delete=models.CASCADE, )
    
    def __str__(self):
        return self.name


class Address(models.Model):
    """Адрес пользователя"""
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Регион', )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    post = models.ForeignKey(Postcode, on_delete=models.SET_NULL, null=True, verbose_name='Почтовый индекс', blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, )
    building = models.CharField(max_length=5, verbose_name='Строение')
    room = models.CharField(max_length=5, verbose_name='Номер квартиры', null=True, blank=True)
    metro = models.ForeignKey(Metro, on_delete=models.SET_NULL, null=True, blank=True)
    map_link = models.URLField(verbose_name='Ссылка на карту', null=True, blank=True)
    corporate_phone = models.CharField(max_length=15, verbose_name='Корпоративный номер телефона', null=True,
                                       blank=True)
    # url_link =
    email = models.EmailField(null=True, blank=True)
    office = models.CharField(max_length=5, null=True, verbose_name='Номер офиса', blank=True)
    time = models.CharField(max_length=30, verbose_name='Рабочее время', null=True, blank=True)
    liter = models.CharField(max_length=200, verbose_name='Литeра', null=True, blank=True)
    
    def __str__(self):
        return f'{self.id}, {self.city}, {self.street}, {self.building}'


class Profile(models.Model):
    user = models.OneToOneField(
        OtivaUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='user'
    )
    
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    
    surname = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    
    phone_num = models.CharField(
        max_length=20,
        verbose_name='номер телефона',
    )
    
    working_position = models.CharField(
        max_length=200,
        verbose_name='Должность'
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
    )
    
    def __str__(self):
        return f'Профайл для {self.user.username}'
