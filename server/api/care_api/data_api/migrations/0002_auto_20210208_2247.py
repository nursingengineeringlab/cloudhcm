# Generated by Django 3.1.6 on 2021-02-08 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rr_data',
            old_name='user',
            new_name='senior',
        ),
        migrations.RenameField(
            model_name='spo2_data',
            old_name='user',
            new_name='senior',
        ),
        migrations.RenameField(
            model_name='temperature_data',
            old_name='user',
            new_name='senior',
        ),
    ]