# Generated by Django 2.2.7 on 2020-01-28 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rnapuzzles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='challenge',
            options={'ordering': ['-puzzle_info', '-created_at'], 'permissions': [('metrics_challenge', 'Run computation of metrics')]},
        ),
    ]
