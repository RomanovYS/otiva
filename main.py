import os

import views
from framework.core import Application

root = os.getcwd() + '\\html'

folders_tree = {
    'root': root,
    'static': root + '\\static\\',
    'pictures': root + '\\pictures\\',
    'templates': root + '\\templates\\'
}

urlpatterns = {
    '/': views.main_view,
    '/about': views.about_view,
    '/about/': views.about_view,
    '/contacts': views.contacts_view,
    '/contacts/': views.contacts_view,
    '/register': views.register_view,
    '/register/': views.register_view,
    '/info': views.info_view,
    '/info/': views.info_view,
    '*': views.page_404_view
}


def secret_controller(request):
    request['secret_key'] = 'SECRET'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)


# waitress-serve --listen=127.0.0.1:8000 main:application
