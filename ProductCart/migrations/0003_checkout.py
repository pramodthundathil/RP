# Generated by Django 3.2.14 on 2023-03-26 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0005_profiledata'),
        ('ProductCart', '0002_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('status', models.CharField(max_length=255)),
                ('py_status', models.BooleanField(default=False)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
