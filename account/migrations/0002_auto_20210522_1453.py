# Generated by Django 3.1.1 on 2021-05-22 06:53

from django.db import migrations, models
import elephant.utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(default=1111111, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.FileField(default=True, null=True, upload_to=elephant.utils.utils.PathAndRename('account/avatar')),
        ),
    ]
