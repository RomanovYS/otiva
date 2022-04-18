from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView

from advertisement_app.forms import TechAdvertisementCreateForm, TechAdvertisementEditForm
from advertisement_app.models import TechAdvertisement, TechPhoto


class TechAdvertisementDetailView(DetailView):
    """Страница объявления"""

    model = TechAdvertisement
    template_name = 'advertisement_app/detail.html'

    def get_context_data(self, **kwargs):
        self.object.increment_views_count()
        return super(TechAdvertisementDetailView, self).get_context_data(**kwargs)


class TechAdvertisementCreateView(FormView):
    """Создание объявления"""

    template_name = 'advertisement_app/create.html'
    form_class = TechAdvertisementCreateForm
    slug = None

    def form_valid(self, form):
        new_advertisement = TechAdvertisement(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            condition=form.cleaned_data['condition'],
            placement_period=form.cleaned_data['placement_period'],
            price=form.cleaned_data['price'],
            creator=self.request.user,
        )
        new_advertisement.save()
        new_advertisement.slug = TechAdvertisement.create_slug(new_advertisement.title, new_advertisement.id)

        # для каждого заргуженного фото создаём объект и записть в бд. 
        # Затем связываем many-to-many с объектом объявления
        for photo in self.request.FILES.getlist('photos'):
            new_photo = TechPhoto.objects.create(photo=photo)
            new_photo.save()
            new_advertisement.photos.add(new_photo)

        new_advertisement.save()
        self.slug = new_advertisement.slug

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('advertisement_app:tech_ad_detail', kwargs={'slug': self.slug})


class TechAdvertisementEditView(UpdateView):
    """Страница редактирования объявления"""
    
    model = TechAdvertisement
    template_name = 'advertisement_app/edit.html'
    form_class = TechAdvertisementEditForm

    def get_success_url(self, **kwargs):
        return reverse('advertisement_app:tech_ad_detail', kwargs={'slug': self.object.slug})
