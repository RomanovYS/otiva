# Generated by Django 3.2.12 on 2022-04-13 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otivauser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email'),
        ),
    ]
