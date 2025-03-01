# Generated by Django 4.2.9 on 2025-01-28 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_courserule_delete_coresubjectrule'),
    ]

    operations = [
        migrations.AddField(
            model_name='courserule',
            name='add_on_courses',
            field=models.ManyToManyField(blank=True, limit_choices_to={'course_type': 'add_on'}, related_name='add_on_course_rules', to='home.course'),
        ),
        migrations.AddField(
            model_name='courserule',
            name='add_on_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='add_on_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='core_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='core_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='elective_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='elective_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='honor_courses',
            field=models.ManyToManyField(blank=True, limit_choices_to={'course_type': 'honor'}, related_name='honor_course_rules', to='home.course'),
        ),
        migrations.AddField(
            model_name='courserule',
            name='honor_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='honor_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='minor_courses',
            field=models.ManyToManyField(blank=True, limit_choices_to={'course_type': 'minor'}, related_name='minor_course_rules', to='home.course'),
        ),
        migrations.AddField(
            model_name='courserule',
            name='minor_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='minor_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='open_elective_courses',
            field=models.ManyToManyField(blank=True, limit_choices_to={'course_type': 'open_elective'}, related_name='open_elective_course_rules', to='home.course'),
        ),
        migrations.AddField(
            model_name='courserule',
            name='open_elective_max_credits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='courserule',
            name='open_elective_min_credits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
