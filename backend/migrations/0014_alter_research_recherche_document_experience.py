# Generated by Django 5.0.2 on 2024-03-22 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_enterprise_etudiant_event_professor_research'),
    ]

    operations = [
        migrations.AlterField(
            model_name='research',
            name='recherche_document',
            field=models.FileField(blank=True, null=True, upload_to='research_documents/'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_debut', models.DateField(auto_now_add=True)),
                ('date_fin', models.DateField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, default='profile_pictures/jobs.png', upload_to='Experiences_images/')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.utilisateur')),
            ],
        ),
    ]
