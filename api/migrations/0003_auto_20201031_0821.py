# Generated by Django 3.1.2 on 2020-10-31 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201031_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='parents',
            new_name='connection',
        ),
    ]