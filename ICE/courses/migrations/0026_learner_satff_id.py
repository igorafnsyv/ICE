# Generated by Django 2.1.7 on 2019-03-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_auto_20190324_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='satff_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]