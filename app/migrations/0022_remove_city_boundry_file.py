# Generated by Django 5.1.3 on 2024-12-13 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_location_boundry_color_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='boundry_file',
        ),
    ]
