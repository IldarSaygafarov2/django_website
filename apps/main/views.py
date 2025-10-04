from django.shortcuts import render, redirect
from .models import Category, FAQ, Article, Like, Dislike, ArticleViewsCount
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'main/article_confirm_delete.html'
    success_url = '/'
    pk_url_kwarg = 'article_id'


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'main/article_form.html'
    form_class = ArticleForm
    success_url = ''
    pk_url_kwarg = 'article_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()  # словарь контекста от UpdateView
        prefix = 'Создать' if 'create' in self.request.path else 'Изменить'
        context['prefix'] = prefix
        return context


def show_home_page(request):
    articles = Article.objects.all()

    paginator = Paginator(articles, 3)
    page = request.GET.get('page')  # 2
    articles = paginator.get_page(page)

    context = {
        'articles': articles
    }
    return render(request, "main/index.html", context)


def show_contacts_page(request):
    return render(request, "main/contacts.html")


def show_category_page(request, category_id):
    # Model.objects.filter() = отдает список совпадающих значений
    # Model.objects.get() = отдает одно совпадающее значение или ошибку

    query = request.GET.get('sort', 'id')

    if category_id == 0:
        category = 'Все категории'
        articles = Article.objects.all().order_by(query)
    else:
        category = Category.objects.get(pk=category_id)
        articles = Article.objects.filter(category=category).order_by(query)

    sorting_fields = {
        'По названию': ['title', '-title'],
        'По просмотрам': ['views', '-views'],
        'По дате': ['created_at', '-created_at'],
    }

    paginator = Paginator(articles, 8)
    page = request.GET.get('page')  # 2
    articles = paginator.get_page(page)

    context = {
        'category': category,
        'articles': articles,
        'sorting_fields': sorting_fields
    }
    return render(request, 'main/category_page.html', context)


def show_article_page(request, article_id):
    article = Article.objects.get(pk=article_id)

    try:
        article.likes  # обращаемся к лайкам статьи
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('article-page', article_id)
    else:
        form = CommentForm()

    # get_or_create
    if request.user.is_authenticated:
        viewed_article, created = ArticleViewsCount.objects.get_or_create(article=article, user=request.user)

        if created:
            article.views += 1
            article.save()
    context = {
        'article': article,
        'form': form
    }
    return render(request, "main/article_page.html", context)


# accounts/login/ users/login/

@login_required(login_url='login-page')
def show_article_form_page(request):
    prefix = 'Создать' if 'create' in request.path else 'Изменить'
    # if not request.user.is_authenticated:
    #     return redirect('login-page')

    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)  # commit=False - предотвращает отправку данных в базу
            form.author = request.user
            form.save()
            return redirect('article-page', form.pk)
    else:
        form = ArticleForm()

    context = {
        'prefix': prefix,
        'form': form
    }
    return render(request, "main/article_form.html", context)


# сделать переход на профиль пользователя
# 1) создать шаблон profile.html внутри приложения users
# 2) создать функцию внутри views.py приложения users (request, username)
# 3) добавить новую ссылку в urls.py внутри приложения users (<str:username>)
# 4) Добавить кнопку в _header.html которая видна только авторизованным пользователям
# 5) в href вызвать url и указать название новой ссылки

# models.py
# views.py
# _info.html

# add_like
# add_dislike

def add_like_or_dislike(request, article_id, action):
    article = Article.objects.get(id=article_id)

    if action == 'add_like':
        # article.likes.user.all() - список пользователей которые поставили лайк
        if request.user in article.likes.user.all():
            article.likes.user.remove(request.user.id)  # убираем пользователя из списка тех, кто добавил лайк
        else:
            article.likes.user.add(request.user.id)
            article.dislikes.user.remove(request.user.id)
    elif action == 'add_dislike':
        if request.user in article.dislikes.user.all():
            article.dislikes.user.remove(request.user.id)
        else:
            article.dislikes.user.add(request.user.id)
            article.likes.user.remove(request.user.id)
    return redirect('article-page', article.id)


def show_faq_page(request):
    return render(request, 'main/faqs.html')


def search(request):
    query = request.GET.get('q')
    articles = Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles
    }
    return render(request, 'main/search.html', context)