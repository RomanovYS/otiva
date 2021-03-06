# Generated by Django 3.2.12 on 2022-05-29 14:10

from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_model', models.CharField(max_length=100, verbose_name='Модель аппарата')),
                ('params', models.TextField(blank=True, null=True, verbose_name='какие-то параметры')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Firm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название фирмы')),
                ('inn', models.IntegerField(verbose_name='ИНН Компании')),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(choices=[('Новый', 'Новый'), ('Б/У', 'Б/У')], default='Новый', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='Цена')),
                ('posted', models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')),
                ('period', models.SmallIntegerField(default=30, verbose_name='Размещено на срок')),
                ('active', models.BooleanField(default=False, verbose_name='Идут показы')),
                ('verified', models.BooleanField(default=False, verbose_name='Проверено модератором')),
                ('description', models.TextField(blank=True, default='Нет описания', null=True, verbose_name='Описание товара')),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.device', verbose_name='Конкретный экземпляр техники')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('country', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200, verbose_name='Заголовок характеристики')),
                ('column1', models.CharField(max_length=500, null=True)),
                ('column2', models.CharField(max_length=500, null=True)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.good')),
            ],
        ),
        migrations.CreateModel(
            name='GoodPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to=main_app.models.get_file_path, verbose_name='Изображение товара')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_photos', to='main_app.good')),
            ],
        ),
    ]
