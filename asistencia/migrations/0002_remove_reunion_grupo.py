# Generated by Django 5.2.1 on 2025-05-28 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reunion',
            name='grupo',
        ),
    ]
