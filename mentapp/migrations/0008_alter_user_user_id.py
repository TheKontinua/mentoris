# Generated by Django 4.2.5 on 2023-11-16 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentapp', '0007_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default='11335783-761f-4b53-9c5d-5f14979f6502', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]