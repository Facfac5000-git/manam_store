# Generated by Django 3.0.8 on 2021-05-20 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20210520_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='days',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
