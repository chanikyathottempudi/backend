import os
import django
from django.urls import get_resolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def list_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            list_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            print(prefix + str(pattern.pattern))

list_urls(get_resolver().url_patterns)
