# Generated by Django 3.1 on 2020-09-07 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0052_pagelogentry'),
        ('blog', '0019_auto_20200907_1430'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DevJournalPage',
        ),
    ]
