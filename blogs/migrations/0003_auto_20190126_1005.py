# Generated by Django 2.1.2 on 2019-01-26 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_bloguser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='matric_card',
            field=models.CharField(max_length=9),
        ),
    ]
