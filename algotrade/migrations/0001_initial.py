# Generated by Django 4.2.7 on 2024-07-11 08:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStrategy',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('strategy_id', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('description', models.TextField()),
                ('advantages', models.TextField()),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_strategy', to='users.user', verbose_name='User-Strategy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserOrders',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_id', models.CharField(max_length=50)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to='users.user', verbose_name='User-Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
