# Generated by Django 4.1.4 on 2023-01-03 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_isactive"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="user",
            table="company",
        ),
    ]
