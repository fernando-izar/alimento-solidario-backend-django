# Generated by Django 4.1.3 on 2023-01-02 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_rename_created_at_donations_createdat_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donations',
            old_name='classification',
            new_name='classification_id',
        ),
    ]
