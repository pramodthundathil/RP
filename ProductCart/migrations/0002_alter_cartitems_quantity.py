# Generated by Django 3.2.14 on 2023-03-26 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductCart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
