# Generated by Django 2.1.2 on 2019-01-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_auto_20190129_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='liked_posts',
            field=models.ManyToManyField(null=True, to='blogs.Post'),
        ),
    ]