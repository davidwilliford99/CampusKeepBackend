# Generated by Django 4.2.6 on 2023-11-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campuskeepbackend', '0013_remove_claim_description_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_found',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]