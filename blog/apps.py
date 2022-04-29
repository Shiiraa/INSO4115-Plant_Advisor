from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

# NEW
class AddressesConfig(AppConfig):
    name = 'addresses'
