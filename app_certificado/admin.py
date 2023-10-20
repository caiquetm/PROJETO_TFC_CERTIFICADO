from django.contrib import admin

from .models import Usuario, Aluno, Certificado, Template

# Register your models here.
class AlunooAdmin(admin.ModelAdmin):
    pass

admin.site.register(Aluno, AlunooAdmin)


class CertificadoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Certificado, CertificadoAdmin)


class TemplateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Template, TemplateAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usuario, UsuarioAdmin)