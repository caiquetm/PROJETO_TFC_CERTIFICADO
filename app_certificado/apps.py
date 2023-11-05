from django.apps import AppConfig


class AppCertificadoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_certificado'

    def ready(self, *args, **kwargs) -> None:
        import app_certificado.signals
        super_ready = super().ready(*args, **kwargs)
        return super_ready