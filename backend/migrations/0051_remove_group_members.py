# Generated by Django 5.0.3 on 2024-03-24 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0050_alter_certification_nom_certificat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
    ]
