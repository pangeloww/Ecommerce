from django.apps import AppConfig

#Default auto field for the website's basket. Gets a default database model.
class BasketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basket'
