# Generated by Django 3.0.8 on 2021-05-20 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='to_trust',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Buyer'),
        ),
    ]
