# Generated by Django 5.1.3 on 2024-11-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_city_boundry_color_code_city_map_fill_color_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='center_latitude',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='center_longitude',
            field=models.CharField(max_length=20, null=True),
        ),
    ]