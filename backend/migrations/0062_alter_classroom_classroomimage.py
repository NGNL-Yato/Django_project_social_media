# Generated by Django 5.0.2 on 2024-03-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0061_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='ClassRoomimage',
            field=models.FileField(upload_to='classroom_course_images/'),
        ),
    ]
