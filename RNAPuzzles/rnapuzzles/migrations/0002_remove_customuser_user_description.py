# Generated by Django 2.2.9 on 2020-01-04 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rnapuzzles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_description',
        ),
    ]