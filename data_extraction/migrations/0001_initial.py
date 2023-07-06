# Generated by Django 4.2 on 2023-04-27 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailyBestPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('body', models.TextField()),
                ('score', models.IntegerField()),
                ('url', models.URLField()),
                ('created_utc', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostByTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('body', models.TextField()),
                ('topic', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('url', models.URLField()),
                ('created_utc', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PBTComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('topic', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('created_utc', models.DateTimeField(blank=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='data_extraction.postbytopic')),
            ],
        ),
        migrations.CreateModel(
            name='DBPComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('score', models.IntegerField()),
                ('created_utc', models.DateTimeField(blank=True, null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='data_extraction.dailybestpost')),
            ],
        ),
    ]
