# Generated by Django 3.1.2 on 2021-06-03 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210603_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 3, 16, 35, 23, 212626)),
        ),
        migrations.AlterField(
            model_name='workerprofile',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]