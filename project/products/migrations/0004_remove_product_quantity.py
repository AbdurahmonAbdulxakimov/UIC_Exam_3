# Generated by Django 4.2.7 on 2024-04-27 13:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_rename_title_material_name_rename_title_product_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="quantity",
        ),
    ]
