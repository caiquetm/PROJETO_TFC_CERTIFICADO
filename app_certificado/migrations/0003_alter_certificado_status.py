# Generated by Django 4.2.4 on 2023-10-19 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_certificado', '0002_rename_templates_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='Status',
            field=models.BooleanField(default=False),
        ),
    ]