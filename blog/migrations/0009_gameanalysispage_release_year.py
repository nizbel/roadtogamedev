# Generated by Django 3.1 on 2020-09-01 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200828_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameanalysispage',
            name='release_year',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
