# Generated by Django 5.2.1 on 2025-06-24 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_service_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='experience',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
