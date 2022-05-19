# Generated by Django 3.2.13 on 2022-05-19 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_customer_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RenameField(
            model_name='sales',
            old_name='product_id',
            new_name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='quantity',
        ),
    ]
