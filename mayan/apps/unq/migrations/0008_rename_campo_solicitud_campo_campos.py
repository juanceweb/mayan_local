# Generated by Django 3.2.20 on 2023-11-01 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unq', '0007_solicitud_campo_campo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitud_campo',
            old_name='campo',
            new_name='campos',
        ),
    ]
