# Generated by Django 2.2.9 on 2020-01-25 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rnapuzzles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Submitted'), (1, 'Evaluation'), (2, 'Error'), (3, ' Success')], default=0),
        ),
    ]
