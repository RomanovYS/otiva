from django.views.generic import TemplateView

from main_app.models import Good


class MainPageView(TemplateView):
    template_name = 'main_app/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods'] = Good.objects.all()
        return context
