from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from main_app.forms import AddGoodForm, AddDeviceForm, UserPersonalDataForm

from main_app.models import Good, GoodPhoto
from user_app.models import OtivaUser


class MainPageView(TemplateView):
    template_name = 'main_app/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods'] = Good.objects.all()
        return context


class UserCabinetView(LoginRequiredMixin, View):
    """Личный кабинет пользователя"""
    template_name = 'main_app/user_cabinet.html'
    
    def get(self, request):
        user = OtivaUser.objects.get(id=request.user.id)
        
        form = UserPersonalDataForm(initial={
            'user_type': user.user_type,
            'first_name': user.profile.first_name,
            'surname': user.profile.surname,
            'phone': user.profile.phone_num,
            'city': user.address.city,
            'area': user.address.area,
            'post_code': user.address.post,
            'street': user.address.street,
            'building': user.address.building,
            'apartment': user.address.room,
            'metro': user.address.metro,
            # 'map_url':
        })
        
        context = {
            'form': form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserPersonalDataForm(request.POST)
        context = {'form': form}
        user = OtivaUser.objects.get(id=request.user.id)
        images = request.FILES.getlist('avatar')
        
        if form.is_valid():
            print('hello')
            if images:
                user.avatar = images[0]
                
            user.user_type = form.cleaned_data['user_type']
            user.profile.first_name = form.cleaned_data['first_name']
            user.profile.surname = form.cleaned_data['surname']
            user.profile.phone_num = form.cleaned_data['phone']
            user.address.city = form.cleaned_data['city']
            user.address.area = form.cleaned_data['area']
            user.address.post = form.cleaned_data['post_code']
            user.address.street = form.cleaned_data['street']
            user.address.building = form.cleaned_data['building']
            user.address.room = form.cleaned_data['apartment']
            user.address.metro = form.cleaned_data['metro']
            
            user.profile.save()
            user.address.save()
            user.save()
        
        return render(request, self.template_name, context)


class UserGoodsView(LoginRequiredMixin, ListView):
    template_name = 'main_app/user_goods_list.html'
    context_object_name = 'goods'
    model = Good
    
    def get_queryset(self):
        goods = Good.objects.filter(owner=self.request.user)
        return goods


class AddGoodView(LoginRequiredMixin, View):
    """Страница добавления объявления"""
    template_name = 'main_app/add_good_view.html'
    
    def get(self, request):
        form = AddGoodForm(initial={'owner': request.user})
        form.owner = self.request.user
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = AddGoodForm(request.POST)
        
        images = request.FILES.getlist('images')
        
        context = {
            'form': form,
        }
        if form.is_valid():
            print(form.cleaned_data)
            
            new_good = Good()
            new_good.owner = request.user
            new_good.condition = form.cleaned_data['condition']
            new_good.price = form.cleaned_data['price']
            new_good.period = form.cleaned_data['period']
            new_good.description = form.cleaned_data['description']
            new_good.device = form.cleaned_data['model']
            new_good.save()
            
            # сохраняем фотографии устройства
            for i, image in enumerate(images, start=1):
                new_good_photo = GoodPhoto.objects.create(
                    good=new_good,
                    title=f'{new_good.device.dev_model}-{i}',
                    image=image
                )
        
        else:
            render(request, self.template_name, context)
        return redirect(reverse('main_app:my_advert'))


class AddDeviceView(LoginRequiredMixin, View):
    """Добавление нового устройства"""
    template_name = 'main_app/add_device_view.html'
    
    def get(self, request):
        form = AddDeviceForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        
        form = AddDeviceForm(request.POST)
        context = {
            'form': form
        }
        
        if form.is_valid():
            form.save()
            return redirect(reverse('main_app:add_good'))
        else:
            return render(request, self.template_name, context)
