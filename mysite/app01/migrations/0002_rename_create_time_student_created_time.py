# Generated by Django 4.1.2 on 2022-10-05 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='create_time',
            new_name='created_time',
        ),
    ]
