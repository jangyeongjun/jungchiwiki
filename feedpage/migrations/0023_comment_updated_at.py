# Generated by Django 3.0.8 on 2020-08-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0022_auto_20200801_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]