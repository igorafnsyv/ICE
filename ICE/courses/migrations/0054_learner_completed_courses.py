# Generated by Django 2.2 on 2019-04-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0053_auto_20190408_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='learner',
            name='completed_courses',
            field=models.ManyToManyField(blank=True, related_name='learner_completed_course', to='courses.Course'),
        ),
    ]
