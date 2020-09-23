# Generated by Django 3.1 on 2020-09-05 06:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0004_auto_20200826_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_id', models.UUIDField(editable=False)),
                ('client_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('password', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('connected', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='realm',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.AddField(
            model_name='session',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.channel'),
        ),
    ]
