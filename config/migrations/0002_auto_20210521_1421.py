# Generated by Django 3.1.1 on 2021-05-21 14:21

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import rest_framework.utils.encoders


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemconfig',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict, encoder=rest_framework.utils.encoders.JSONEncoder),
        ),
    ]
