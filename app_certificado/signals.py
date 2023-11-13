from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver

from app_certificado.models import Certificado


#def delete_image(instance):
#    try:
#       os.remove(instance.imagem.path)
#   except (ValueError, FileNotFoundError):
#       ...

#@receiver(pre_delete, sender=Certificado)
#def delete_imagens(sender, instance, created, *args, **kwargs):
#    old_instance = Certificado.objects.get(pk=instance.pk)
#   delete_image(old_instance)

@receiver(post_save, sender=Certificado)
def update_aluno_horas(sender, instance, created, **kwargs):
    if created:
        return  # Se for um novo certificado ele pula
    if instance.status == 1:
        instance.update_aluno_horas()



@receiver(post_delete, sender=Certificado)
def subtract_aluno_horas(sender, instance, **kwargs):
    if instance.status == 1 and instance.aluno:
        instance.aluno.horas -= int(instance.duracao)
        instance.aluno.save()