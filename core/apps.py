from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # If your core app folder is at the project root (manage.py is sibling of core), keep 'core'
    name = 'core'
    # If core lives inside your project package (django_project/core), change to:
    # name = 'django_project.core'