# Generated by Django 3.2.20 on 2023-09-27 20:30

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_comments', '0006_auto_20210130_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rol_destino',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, default=list, size=None),
        ),
    ]
