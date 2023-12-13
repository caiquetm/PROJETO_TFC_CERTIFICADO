from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from app_certificado.models import Certificado
from django.db import models


#def delete_image(instance):
#    try:
#       os.remove(instance.imagem.path)
#   except (ValueError, FileNotFoundError):
#       ...

#@receiver(pre_delete, sender=Certificado)
#def delete_imagens(sender, instance, created, *args, **kwargs):
#    old_instance = Certificado.objects.get(pk=instance.pk)
#   delete_image(old_instance)

#@receiver(post_save, sender=Certificado)
#def update_aluno_horas(sender, instance, created, **kwargs):
#    if created:
#        return  # Se for um novo certificado ele pula
#    if instance.status == 1:
#        instance.update_aluno_horas()



@receiver(post_delete, sender=Certificado)
def subtract_aluno_horas(sender, instance, **kwargs):
    if instance.status == 1 and instance.aluno:
        instance.aluno.horas -= int(instance.duracao)
        instance.aluno.save()



@receiver(post_save, sender=Certificado)
@receiver(post_delete, sender=Certificado)
def update_aluno_horas(sender, instance, **kwargs):
    if instance.aluno:
        total_horas = Certificado.objects.filter(aluno=instance.aluno, status=1).aggregate(total_horas=models.Sum('duracao'))['total_horas']
        instance.aluno.horas = total_horas if total_horas else 0
        instance.aluno.save()