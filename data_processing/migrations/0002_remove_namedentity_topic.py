# Generated by Django 4.2 on 2023-04-27 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_processing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='namedentity',
            name='topic',
        ),
    ]
