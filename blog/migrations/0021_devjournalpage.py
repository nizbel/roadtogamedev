# Generated by Django 3.1 on 2020-09-07 17:35

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailtrans', '0009_create_initial_language'),
        ('blog', '0020_delete_devjournalpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevJournalPage',
            fields=[
                ('translatablepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailtrans.translatablepage')),
                ('date', models.DateField(verbose_name='Post date')),
                ('entry_index', models.IntegerField(verbose_name='Entry index')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(template='blocks/paragraph.html'))])),
            ],
            options={
                'unique_together': {('entry_index', 'translatablepage_ptr_id')},
            },
            bases=('wagtailtrans.translatablepage',),
        ),
    ]
