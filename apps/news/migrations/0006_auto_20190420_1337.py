# Generated by Django 2.0 on 2019-04-20 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20190420_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['priority']},
        ),
        migrations.RenameField(
            model_name='banner',
            old_name='position',
            new_name='priority',
        ),
    ]
