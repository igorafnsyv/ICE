# Generated by Django 2.1.7 on 2019-03-25 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_learner_satff_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='learner',
            old_name='satff_id',
            new_name='staff_id',
        ),
    ]
