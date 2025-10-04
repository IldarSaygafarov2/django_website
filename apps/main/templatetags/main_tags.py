from apps.main.models import Category, FAQ

from django.template import Library


# объект для проверки того, что функция загружается в html файлах
register = Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_faqs():
    return FAQ.objects.all()