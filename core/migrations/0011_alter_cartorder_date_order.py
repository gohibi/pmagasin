# Generated by Django 5.0.3 on 2024-04-12 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_cartorder_date_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='date_order',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
