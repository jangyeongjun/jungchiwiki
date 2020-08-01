# Generated by Django 3.0.8 on 2020-07-31 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0012_merge_20200730_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commenttocomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ctc', to='feedpage.Comment'),
        ),
        migrations.AlterField(
            model_name='politician',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]