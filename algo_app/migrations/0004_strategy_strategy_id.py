# Generated by Django 4.2.7 on 2024-02-28 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algo_app', '0003_wallet_strategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='strategy_id',
            field=models.CharField(blank=True, default=None, max_length=40, null=True),
        ),
    ]