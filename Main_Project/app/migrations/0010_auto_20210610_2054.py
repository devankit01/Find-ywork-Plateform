# Generated by Django 3.0.14 on 2021-06-10 15:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210610_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 10, 20, 54, 31, 555867)),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(max_length=10)),
                ('feedback', models.TextField()),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Work')),
            ],
        ),
    ]