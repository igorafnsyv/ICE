# Generated by Django 2.1.7 on 2019-04-06 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0048_auto_20190406_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
