from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View

from user_app.forms import OtivaUserLoginForm, OtivaUserRegisterForm
from user_app.models import OtivaUser


class OtivaUserRegisterView(View):
    """Регистрация пользователя"""
    
    template_view = 'user_app/register.html'
    form = OtivaUserRegisterForm
    
    def send_verify_email(self, user: OtivaUser):
        """Отправка сообщения с кодом активации"""
        verify_link = 1  # todo: поменять
        title = f'Активация пользователя {user.username} на портале Otiva Project'
        message = f'Для активации вашей учетной записи {user.username} на портале Otiva Project ' \
                  f'{settings.DOMAIN_NAME}' \
                  f'перейдите по ссылке:\n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
    
    def get(self, request):
        return render(request, self.template_view, {'form': self.form})
    
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            
            ########
            # сразу активируем пользователя
            user.is_active = True
            user.save()
            ###########
            
            print(f'user {user.username} saved')
            return HttpResponseRedirect(reverse('user_app:login'))
        print(form.error_messages)
        return render(request, self.template_view, {'form': form})


class OtivaUserLoginView(LoginView):
    authentication_form = OtivaUserLoginForm
    template_name = 'user_app/login.html'


class OtivaUserLogoutView(LogoutView):
    template_name = 'user_app/logout.html'
    next_page = '/'
