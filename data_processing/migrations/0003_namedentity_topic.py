# Generated by Django 4.2 on 2023-04-27 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_processing', '0002_remove_namedentity_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='namedentity',
            name='topic',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]