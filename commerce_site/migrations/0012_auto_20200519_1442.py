# Generated by Django 3.0.4 on 2020-05-19 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce_site', '0011_auto_20200519_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
