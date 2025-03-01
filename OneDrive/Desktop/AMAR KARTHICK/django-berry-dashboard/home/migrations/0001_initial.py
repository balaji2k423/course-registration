# Generated by Django 4.2.9 on 2024-12-23 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='dishes/')),
                ('category', models.CharField(max_length=100, null=True)),
                ('preparation_time', models.DurationField(default=0)),
                ('tags', models.ManyToManyField(blank=True, related_name='dishes', to='home.tag')),
            ],
        ),
    ]
