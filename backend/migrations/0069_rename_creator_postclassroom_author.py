# Generated by Django 5.0.2 on 2024-03-29 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0068_merge_20240329_2037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postclassroom',
            old_name='creator',
            new_name='author',
        ),
    ]
