# Generated by Django 3.0.4 on 2020-05-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce_site', '0016_auto_20200523_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
