# Generated by Django 3.0.6 on 2020-10-08 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
