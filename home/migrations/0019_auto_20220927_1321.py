# Generated by Django 3.1 on 2022-09-27 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_resumepage_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumepage',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]
