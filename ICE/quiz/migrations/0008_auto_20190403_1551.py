# Generated by Django 2.1.7 on 2019-04-03 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_quizbank_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizbank',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Module'),
        ),
    ]
