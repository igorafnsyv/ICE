# Generated by Django 2.1.7 on 2019-04-03 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0038_learner_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
