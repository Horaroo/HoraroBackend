# Generated by Django 4.0.5 on 2022-07-04 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("schedules", "0002_userprofile_telegram_id"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BlockUser",
        ),
    ]