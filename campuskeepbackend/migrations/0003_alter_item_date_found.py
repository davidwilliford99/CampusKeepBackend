# Generated by Django 4.2.6 on 2023-11-01 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campuskeepbackend', '0002_message_claim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_found',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
