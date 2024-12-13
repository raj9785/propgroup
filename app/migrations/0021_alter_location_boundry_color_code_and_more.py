# Generated by Django 5.1.3 on 2024-12-13 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_city_boundry_json_location_boundry_json_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='boundry_color_code',
            field=models.CharField(blank=True, default='#000000', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='sequence_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
