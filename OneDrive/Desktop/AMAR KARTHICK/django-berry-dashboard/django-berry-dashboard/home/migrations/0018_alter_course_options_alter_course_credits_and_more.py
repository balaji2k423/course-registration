# Generated by Django 4.2.9 on 2025-01-27 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_course_semester'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['department', 'semester', 'course_code'], 'verbose_name': 'Course', 'verbose_name_plural': 'Courses'},
        ),
        migrations.AlterField(
            model_name='course',
            name='credits',
            field=models.DecimalField(decimal_places=1, editable=False, max_digits=3),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecture_points',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='L'),
        ),
        migrations.AlterField(
            model_name='course',
            name='practical_points',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='P'),
        ),
        migrations.AlterField(
            model_name='course',
            name='tutorial_points',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3, verbose_name='T'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('course_code', 'academic_year')},
        ),
    ]
