# Generated by Django 5.0.7 on 2024-10-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_grouptoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptoken',
            name='admin',
            field=models.CharField(default='', max_length=100),
        ),
    ]
