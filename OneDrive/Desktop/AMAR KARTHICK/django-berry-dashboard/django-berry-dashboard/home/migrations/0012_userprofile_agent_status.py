# Generated by Django 4.2.9 on 2025-01-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_orderstatus_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='agent_status',
            field=models.BooleanField(default=False),
        ),
    ]
