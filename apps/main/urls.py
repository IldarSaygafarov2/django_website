# http://127.0.0.1:8000/
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),
    path('contacts/', views.show_contacts_page, name='contacts'),
    path('faqs/', views.show_faq_page, name='faqs'),
    path('search/', views.search, name='search'),
    path('categories/<int:category_id>/', views.show_category_page, name='category-page'),
    path('articles/<int:article_id>/', views.show_article_page, name='article-page'),
    path('articles/<int:article_id>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('articles/<int:article_id>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<int:article_id>/<str:action>/', views.add_like_or_dislike, name='vote'),
    path('create/', views.show_article_form_page, name='create-article')
]

