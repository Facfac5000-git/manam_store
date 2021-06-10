# Generated by Django 3.0.8 on 2021-05-20 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_buyer_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='days',
        ),
        migrations.AddField(
            model_name='supplier',
            name='days',
            field=models.CharField(default='l', max_length=100),
            preserve_default=False,
        ),
    ]