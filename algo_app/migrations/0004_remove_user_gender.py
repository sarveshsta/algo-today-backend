# Generated by Django 4.2.7 on 2024-02-13 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algo_app', '0003_user_gender_user_groups_user_is_active_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
