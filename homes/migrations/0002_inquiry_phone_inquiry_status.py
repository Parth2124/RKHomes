# Generated by Django 5.2 on 2025-06-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Talked', 'Talked')], default='Pending', max_length=10),
        ),
    ]
