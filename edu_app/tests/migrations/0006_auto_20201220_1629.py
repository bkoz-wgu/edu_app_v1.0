# Generated by Django 3.1.4 on 2020-12-20 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_auto_20201220_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_data',
            name='graded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='test_data',
            name='score',
            field=models.CharField(default=0, max_length=3),
        ),
    ]
