# Generated by Django 4.2.10 on 2024-02-27 16:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senseiapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='areas_of_expertise',
        ),
        migrations.DeleteModel(
            name='AreaOfExpertise',
        ),
        migrations.AddField(
            model_name='teacher',
            name='areas_of_expertise',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None),
        ),
    ]
