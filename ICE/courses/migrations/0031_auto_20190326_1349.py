# Generated by Django 2.1.7 on 2019-03-26 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_remove_module_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='component',
            old_name='date_update',
            new_name='date_updated',
        ),
    ]
