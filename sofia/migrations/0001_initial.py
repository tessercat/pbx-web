# Generated by Django 3.2.2 on 2021-05-18 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SofiaProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(unique=True)),
                ('domain', models.SlugField(unique=True)),
            ],
        ),
    ]
