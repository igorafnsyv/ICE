# Generated by Django 2.1.7 on 2019-03-20 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20190320_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Module'),
        ),
    ]
