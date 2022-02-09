import main
from framework.templates import render


def main_view(request):
    secret = request.get('secret_key', None)
    return '200 OK', render(path=main.folders_tree['templates'], template='index.html', secret=secret)


def about_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='about.html')


def contacts_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='contacts.html')


def register_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='register.html')


def page_404_view():
    return '404 NOT FOUND', render(path=main.folders_tree['templates'], template='page404.html')
