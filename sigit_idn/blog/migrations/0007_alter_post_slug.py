# Generated by Django 3.2 on 2022-04-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20220402_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='<django.db.models.fields.charfield>', max_length=200, unique=True),
        ),
    ]
