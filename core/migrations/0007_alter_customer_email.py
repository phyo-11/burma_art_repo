# Generated by Django 5.1.4 on 2025-01-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_product_description_alter_product_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
