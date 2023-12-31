# Generated by Django 4.2.4 on 2023-10-20 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_certificado', '0004_usuario_adm_alter_certificado_imagem_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aluno',
            old_name='Horas',
            new_name='horas',
        ),
        migrations.RenameField(
            model_name='aluno',
            old_name='Nome',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Aluno',
            new_name='aluno',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Categoria',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Duracao',
            new_name='duracao',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Imagem',
            new_name='imagem',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Instituicao',
            new_name='instituicao',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Nome',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='Templates',
            new_name='template',
        ),
        migrations.RenameField(
            model_name='template',
            old_name='Imagem',
            new_name='imagem',
        ),
        migrations.RenameField(
            model_name='template',
            old_name='Instituicao',
            new_name='instituicao',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='Adm',
            new_name='adm',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='Nome',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='Senha',
            new_name='senha',
        ),
    ]
