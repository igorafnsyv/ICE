# Generated by Django 2.1.7 on 2019-04-03 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0036_auto_20190403_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learner',
            name='user',
        ),
    ]