from django.apps import AppConfig



class RnapuzzlesConfig(AppConfig):
    name = 'rnapuzzles'

    def ready(self):
        import rnapuzzles.signals
