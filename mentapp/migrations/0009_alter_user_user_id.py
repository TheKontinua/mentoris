# Generated by Django 4.2.6 on 2023-11-16 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentapp', '0008_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default='68113fbd-e2e1-4e58-a27c-6628b482d8ae', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
