# Generated by Django 3.0.6 on 2020-08-01 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0021_merge_20200801_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='law',
            old_name='propse_dt',
            new_name='propose_dt',
        ),
    ]
