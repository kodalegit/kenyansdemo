import json
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from ...models import Articles

class Command(BaseCommand):
    help = 'Export articles to a JSON file'

    def handle(self, *args, **options):
        # Query all articles from the database
        articles_queryset = Articles.objects.all()

        # Serialize the queryset to JSON
        articles_json = serialize('json', articles_queryset)

        # Write JSON data to a file
        json_file_path = 'articles.json'
        with open(json_file_path, 'w') as json_file:
            json_file.write(articles_json)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported articles to {json_file_path}'))