# Generated by Django 5.0.6 on 2024-06-27 07:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0007_college_uuid_university_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
