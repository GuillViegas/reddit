# Generated by Django 3.0.7 on 2020-10-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_auto_20201016_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reddituser',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
