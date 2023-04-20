# Generated by Django 4.0.1 on 2023-04-20 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0005_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='email',
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default='jaivardhan@gmail.com', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='email'),
        ),
    ]
