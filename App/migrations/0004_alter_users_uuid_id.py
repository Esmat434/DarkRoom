# Generated by Django 5.0.7 on 2024-09-28 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='uuid_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
