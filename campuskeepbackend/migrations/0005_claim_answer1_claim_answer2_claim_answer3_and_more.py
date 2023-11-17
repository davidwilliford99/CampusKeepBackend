# Generated by Django 4.2.6 on 2023-11-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campuskeepbackend', '0004_alter_item_date_found'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='answer1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='answer2',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='answer3',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
    ]
