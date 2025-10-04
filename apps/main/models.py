from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# ORM - object relation model

# Category
# main_название_таблицы

# main_category
# name = str

"""
create table if not exists main_category(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
"""


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # название модели в единственном числе
        verbose_name_plural = 'Категории'  # название модели во множественном числе


# python manage.py makemigrations
# python manage.py migrate

# создать класс FAQ
# question - models.CharField
# answer - models.TextField
# строковое представление
# название модели в ед.числе
# название модели во мн.числе
# регистрируете в admin.py


class FAQ(models.Model):
    question = models.CharField(max_length=64, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание', blank=True, null=True)
    full_description = models.TextField(verbose_name='Полное описание')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_visible = models.BooleanField(default=True, verbose_name='Статья активна?')
    preview = models.ImageField(upload_to='previews/articles/',
                                verbose_name='Заставка', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-page', kwargs={'article_id': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

# сделать так. чтобы эта модель, была видна в админ панели
# строковое представление
# класс Meta (verbose_name, verbose_name_plural)
# создать миграцию
# Выполнить миграцию
# зарегистрировать модель в admin.py


# добавить модель Comment
# text
# author
# article
# created_at
# добавить строкове представление
# добавить class Meta
# зарегистрировать модель в админ панели

class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.text[:30]}...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

# media/articles/article_id/image.jpg

def make_article_image_path(instance, filename):
    return f'articles/{instance.article.pk}/{filename}'


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    image = models.ImageField(upload_to=make_article_image_path, verbose_name='Фотография')


class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')


class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')


class ArticleViewsCount(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

