# Generated by Django 4.2.10 on 2024-02-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senseiapp', '0005_alter_teacher_student_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='student_list',
            field=models.ManyToManyField(null=True, to='senseiapp.student'),
        ),
    ]
