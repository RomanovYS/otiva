from django.db import models

from user_app.models import OtivaUser


class TechPhoto(models.Model):
    photo = models.ImageField(upload_to='tech_images/')


class TechAdvertisement(models.Model):
    """Модель объявления техники"""

    tech_conditions = (
        # Brand New
        ('NEW', 'Новый'),
        # Used
        ('USD', 'Б/У (рабочий)'),
        # Broken
        ('BKN', 'Б/У (не рабочий)'),
    )

    periods = (
        (30, '30 дней'),
        (60, '60 дней'),
        (120, '120 дней'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.CharField(max_length=3, choices=tech_conditions, default='NEW')
    placement_period = models.PositiveIntegerField(choices=periods, default=30)
    price = models.PositiveIntegerField()
    views_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(OtivaUser, on_delete=models.CASCADE)
    photos = models.ManyToManyField(TechPhoto, blank=True, null=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_slug(title, id):
        """Создаём slug из первых трёх слов названия объявления"""

        words = title.split(' ')
        if len(words) > 3:
            words = words[:3]
        return f'{"-".join([word.lower() for word in words])}-{id}'

    def increment_views_count(self):
        self.views_count += 1
        self.save()
