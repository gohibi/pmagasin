# Generated by Django 5.0.3 on 2024-04-03 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='life',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stock_count',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
