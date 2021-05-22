# Generated by Django 3.2.2 on 2021-05-22 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('verto', '0001_initial'),
        ('sofia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension_number', models.CharField(max_length=50)),
                ('web_enabled', models.BooleanField(default=False)),
                ('channel', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='verto.channel')),
                ('intercom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sofia.intercom')),
            ],
        ),
        migrations.CreateModel(
            name='GatewayExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('expression', models.CharField(max_length=50)),
                ('cid_name', models.CharField(max_length=50)),
                ('cid_number', models.CharField(max_length=50)),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sofia.gateway')),
                ('intercom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sofia.intercom')),
            ],
        ),
        migrations.CreateModel(
            name='Bridge',
            fields=[
                ('action_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='intercom.action')),
            ],
            bases=('intercom.action',),
        ),
        migrations.CreateModel(
            name='InboundTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('transfer_extension', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intercom.extension')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='extension',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intercom.extension'),
        ),
        migrations.CreateModel(
            name='OutsideLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=50, unique=True)),
                ('cid_name', models.CharField(max_length=50)),
                ('cid_number', models.CharField(max_length=50)),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sofia.gateway')),
                ('bridges', models.ManyToManyField(blank=True, to='intercom.Bridge')),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('username', models.SlugField()),
                ('password', models.CharField(max_length=50)),
                ('registered', models.DateTimeField(blank=True, null=True)),
                ('gateway_extensions', models.ManyToManyField(blank=True, to='intercom.GatewayExtension')),
                ('intercom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sofia.intercom')),
                ('bridges', models.ManyToManyField(blank=True, to='intercom.Bridge')),
            ],
        ),
        migrations.AddConstraint(
            model_name='gatewayextension',
            constraint=models.UniqueConstraint(fields=('expression', 'intercom'), name='intercom_gatewayextension_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='extension',
            constraint=models.UniqueConstraint(fields=('extension_number', 'intercom'), name='intercom_extension_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='line',
            constraint=models.UniqueConstraint(fields=('username', 'intercom'), name='per_intercom_unique_username'),
        ),
    ]
