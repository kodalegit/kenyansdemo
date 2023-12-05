from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .models import Articles
from django.views import View
from openai import OpenAI
from django.conf import settings

# Article entry form
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            'title',
            'body',
            'author',
            'image_url',
        ]
        labels = {
            'title': 'Viral Title',
            'body': 'Body',
            'author': 'Author',
            'image_url': 'Image URL',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.TextInput(attrs={'class':'form-control', 'rows': 5}),
            'author': forms.TextInput(attrs={'class':'form-control'}),
            'image_url': forms.TextInput(attrs={'class':'form-control'}),
        }

class ArticleDetailView(View):
    template_name = 'ai/article_detail.html'

    def get(self, request, link):
        article = get_object_or_404(Articles, link=link)
        return render(request, self.template_name, {'article': article})


def index(request):
    articles = Articles.objects.all().order_by('-time')

    # Extract introduction for display.
    for article in articles:
        first_sentence = extract_sentence(article.body)
        article.body = first_sentence

    return render(request, 'ai/index.html', {
        'articles': articles,
    })

def extract_sentence(text):
    sentences = text.split('.')
    if sentences:
        return sentences[0].strip() + '.'
    
    return ''

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
    
# Initializa assistant
# api_key = settings.API_KEY
# client = OpenAI(api_key=api_key)

# file = client.files.create(
#     file=open("knowledge.pdf", "rb"),
#     purpose='assistants'
# )

# assistant = client.beta.assistants.create(
#     instructions="",
#     name="Summariser",
#     tools=[{"type":"retrieval"}],
#     model="gpt-3.5-turbo-1106",
#     file_ids=[file.id]
# )

# # Start new conversation with ChatGPT
# def start_conversation(request):
#     print('Starting a new converstion...')
#     thread = client.beta.threads.create()
#     print(f'New thread created with ID: {thread.id}')

#     return thread.id




    


