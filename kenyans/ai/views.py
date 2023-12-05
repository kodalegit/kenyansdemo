from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from .models import Articles
from django.views import View
from openai import OpenAI
from django.conf import settings
import time
import os
import json

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
            'body': forms.Textarea(attrs={'class':'form-control', 'rows': 5}),
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
api_key = settings.API_KEY
client = OpenAI(api_key=api_key)

# Check current assistant id
assistant_file_path = 'assistant.json'
if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
        assistant_data = json.load(file)
        assistant_id = assistant_data['assistant_id']
        print("Loaded existing assistant ID")
else:
    # Create new assistant if non-existent
    file = client.files.create(
        file=open("articles.txt", "rb"),
        purpose='assistants'
    )

    assistant = client.beta.assistants.create(
        instructions="You are an informative assistant programmed to summarise news to readers. You are provided with news articles as knowledge and can answer questions about them. Be concise and informative when prompted by the user.",
        name="Summariser",
        tools=[{"type":"retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=[file.id]
    )

    assistant_data = {'assistant_id':assistant.id}
    assistant_id = assistant.id
    with open(assistant_file_path, 'w') as file:
        json.dump(assistant_data, file)
    print('Saved new assistant ID to ', assistant_file_path)

def create_thread():
    print('Starting a new converstion...')
    thread = client.beta.threads.create()
    print(f'New thread created with ID: {thread.id}')

    return thread.id



# Start new conversation with ChatGPT
def start_conversation(request):
    if request.method == 'POST':
        prompt = request.POST["prompt"]
        threads_id = request.POST["thread_id"]

        if not threads_id:
            threads_id = create_thread()

        thread_message = client.beta.threads.messages.create(
        thread_id=threads_id,
        role="user",
        content=prompt,
        )
        print(thread_message)

        # Run the assistant
        run = client.beta.threads.runs.create(thread_id=threads_id, assistant_id=assistant_id)

        # Check if run is complete
        run_status = client.beta.threads.runs.retrieve(thread_id=threads_id, run_id=run.id)
        while run_status.status != 'completed':
            run_status = client.beta.threads.runs.retrieve(thread_id=threads_id, run_id=run.id)
            time.sleep(2)

        response = client.beta.threads.messages.list(thread_id=threads_id)
        answer = response.data[0].content[0].text.value
        role = response.data[0].role
        print(answer)

        return render(request, 'ai/fill.html', {'answer':answer, 'role':role, 'thread_id':threads_id})
    
    return render(request, 'ai/fill.html')



# def chat(request, id):
#     thread_id = start_conversation()

#     # Add user message to thread
#     client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)
    
#     # Run the assistant
#     run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant.id)

#     while True:
#         run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        

#         if run_status.status == 'completed':
#             break
        

    




    


