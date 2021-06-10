# Generated by Django 3.0.8 on 2021-05-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20210520_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('detail', models.TextField(max_length=500)),
                ('amount', models.FloatField()),
                ('type', models.CharField(max_length=10)),
                ('total', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='expire_date',
            field=models.DateField(),
        ),
    ]
