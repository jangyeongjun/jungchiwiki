# Generated by Django 3.0.8 on 2020-07-26 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', '남성'), ('W', '여성')], max_length=1),
        ),
    ]
