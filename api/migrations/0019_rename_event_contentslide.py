# Generated by Django 4.0.5 on 2023-03-18 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_delete_numberweek"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Event",
            new_name="ContentSlide",
        ),
    ]