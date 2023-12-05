from django.urls import path
from . import views
from .views import ArticleDetailView

urlpatterns = [
    path("", views.index, name="index"),
    path("write", views.write, name="write"),
    path('articles/<slug:link>/', ArticleDetailView.as_view(), name='article_detail'),
    # path('start/',views.start_conversation, name='start'),
    # path('chat/',views.chat, name='chat'),
]