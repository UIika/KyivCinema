# Generated by Django 4.2.7 on 2023-12-07 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_ticket_user_alter_session_movie_alter_ticket_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, default='Опис відсутній', null=True, verbose_name='Опис'),
        ),
    ]
