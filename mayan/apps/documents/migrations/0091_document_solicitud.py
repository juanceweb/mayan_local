# Generated by Django 3.2.20 on 2023-09-27 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unq', '0004_auto_20230926_1513'),
        ('documents', '0090_alter_documentversion_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='solicitud',
            field=models.OneToOneField(help_text='solicitud asociada al documento', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud', to='unq.solicitud', verbose_name='solicitud'),
        ),
    ]
