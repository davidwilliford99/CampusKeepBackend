# Generated by Django 4.2.6 on 2023-10-30 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campuskeepbackend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_date', models.DateTimeField(auto_now_add=True)),
                ('claimed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims_made', to=settings.AUTH_USER_MODEL)),
                ('finder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_found', to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='campuskeepbackend.item')),
            ],
        ),
    ]
