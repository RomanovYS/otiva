import main
from framework import core
from framework.templates import render



def main_view(request):
    secret = request.get('secret_key', None)
    print(request)
    return '200 OK', render(path=main.folders_tree['templates'], template='index.html', secret=secret)


def about_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'],
                            template='about.html',
                            courses=core.courses_dict)


def contacts_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='contacts.html')


def register_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='register.html')


def info_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'], template='info.html')


def n_cat_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'],
                            template='new_category.html',
                            categories=core.categories_list)


def n_course_view(request=None):
    return '200 OK', render(path=main.folders_tree['templates'],
                            template='new_course.html',
                            categories=core.categories_list)


def page_404_view():
    return '404 NOT FOUND', render(path=main.folders_tree['templates'], template='page404.html')
