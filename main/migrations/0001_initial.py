# Generated by Django 5.1.1 on 2024-09-26 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SiteStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transitions_count', models.IntegerField(default=0)),
                ('data_sent', models.BigIntegerField(default=0)),
                ('data_received', models.BigIntegerField(default=0)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='main.site')),
            ],
        ),
    ]
