from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .models import Articles

# Article entry form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            'title',
            'body'
        ]
        labels = {
            'title': 'Viral Title',
            'body': 'Body',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.TextInput(attrs={'class':'form-control', 'rows': 5}),
        }

def index(request):
    articles = Articles.objects.all().order_by('-time')
    return render(request, 'ai/index.html', {
        'articles': articles,
    })

def write(request):
    # Save an article to the database
    if request.method == 'POST':
        article = ArticleForm(request.POST)

        if article.is_valid():
            body = article.cleaned_data['body']
            title = article.cleaned_data['title']

            new_article = Articles(title=title, body=body,)
            new_article.save()

        articles = Articles.objects.all().order_by('-time')

        return render(request, 'ai/index.html', {
            'articles': articles
        })
    
    # Load the write page with input form
    articles = Articles.objects.all().order_by('-time')

    return render(request, 'ai/write.html', {
        'form': ArticleForm()
    })
    
