# Generated by Django 3.1 on 2022-09-23 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20220923_0107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamepage',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Technology',
        ),
    ]
