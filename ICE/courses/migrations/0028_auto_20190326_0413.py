# Generated by Django 2.1.7 on 2019-03-26 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0027_auto_20190325_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='position',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
