# Generated by Django 5.0.7 on 2024-10-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_chatdata_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaltoken',
            name='created_time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
