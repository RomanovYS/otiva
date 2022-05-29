import os.path
import uuid

from django.db import models

from user_app.models import OtivaUser


class Manufacturer(models.Model):
    """Производитель"""
    name = models.CharField(max_length=100, unique=True, db_index=True, )
    country = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name


class Firm(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название фирмы')
    inn = models.IntegerField(verbose_name='ИНН Компании')
    
    def __str__(self):
        return self.name


class DeviceType(models.Model):
    type_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.type_name


class Device(models.Model):
    
    dev_model = models.CharField(max_length=100, verbose_name='Модель аппарата')
    dev_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, verbose_name='Тип аппарата')
    manuf = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель')
    params = models.TextField(verbose_name='какие-то параметры', blank=True, null=True)
    
    def __str__(self):
        return self.dev_model


class Good(models.Model):
    """Таблица непосредственно товаров"""

    CONDITIONS = [
        ('Новый', 'Новый'),
        ('Б/У', 'Б/У'),
    ]

    owner = models.ForeignKey(OtivaUser, on_delete=models.CASCADE, verbose_name='Владелец объявления')
    condition = models.CharField(max_length=20, choices=CONDITIONS, default='Новый')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', null=True)
    posted = models.DateTimeField(verbose_name='Дата размещения', auto_now_add=True)
    period = models.SmallIntegerField(verbose_name='Размещено на срок', default=30)
    active = models.BooleanField(default=False, verbose_name='Идут показы')
    verified = models.BooleanField(default=False, verbose_name='Проверено модератором')
    description = models.TextField(blank=True, null=True, default='Нет описания', verbose_name='Описание товара')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='Конкретный экземпляр техники', null=True)
    
    # part_num = verbose_name = 'Номер запчасти', null = True
    def __str__(self):
        return f'{self.device.dev_model} - {self.price}'


class Specification(models.Model):
    """Таблица характеристик товара"""
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200, verbose_name='Заголовок характеристики')
    column1 = models.CharField(max_length=500, null=True)
    column2 = models.CharField(max_length=500, null=True)
    
    def __str__(self):
        return f'{self.good.device.dev_model} - {self.heading}'


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('good_photos', instance.good.owner.username, filename)


class GoodPhoto(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='good_photos')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=get_file_path, verbose_name='Изображение товара', blank=True, null=True)
    
    def __str__(self):
        return self.title
