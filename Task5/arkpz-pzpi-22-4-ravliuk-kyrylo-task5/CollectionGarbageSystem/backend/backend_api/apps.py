from django.apps import AppConfig

# Define the configuration class for the 'backend_api' app
class BackendApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_api'

    def ready(self):
        # Import the signals module to ensure that signals are connected properly when server is running
        import backend_api.api.signals 