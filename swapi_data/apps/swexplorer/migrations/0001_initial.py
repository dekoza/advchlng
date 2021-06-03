# Generated by Django 3.2.3 on 2021-06-02 20:17

from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SwapiCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FilePathField(path=pathlib.PurePosixPath('/app/data_vault'))),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]