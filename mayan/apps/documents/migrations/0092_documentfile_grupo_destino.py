# Generated by Django 3.2.20 on 2023-10-25 17:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0091_document_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='grupo_destino',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, default=list, size=None),
        ),
    ]
