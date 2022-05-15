from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView
from main_app.forms import AddGoodForm

from main_app.models import Good


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
        return render(request, self.template_name)


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
        form = AddGoodForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
