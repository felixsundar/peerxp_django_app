# Generated by Django 4.0.4 on 2022-05-17 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('support_ticket_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='APIToken',
        ),
    ]
