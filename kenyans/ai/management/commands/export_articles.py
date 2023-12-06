from django.core.management.base import BaseCommand
from ...models import Articles

class Command(BaseCommand):
    help = 'Export articles to a txt file'

    def handle(self, *args, **options):
        # Query all articles from the database
        articles_queryset = Articles.objects.all()

        # Prepare the articles as plain text
        plain_text_articles = ""
        for article in articles_queryset:
            plain_text_articles += f"Title: {article.title}\n"
            plain_text_articles += f"Author: {article.author}\n"
            plain_text_articles += f"Time: {article.time}\n"
            plain_text_articles += f"Body: {article.body}\n\n"

        # Write plain text data to a file
        text_file_path = 'articles.txt'
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(plain_text_articles)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported articles to {text_file_path}'))