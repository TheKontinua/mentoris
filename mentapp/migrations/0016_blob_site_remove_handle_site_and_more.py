# Generated by Django 4.2.5 on 2023-11-18 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentapp', '0015_alter_user_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blob',
            fields=[
                ('blob_key', models.BinaryField(default=b'', primary_key=True, serialize=False)),
                ('binary_data', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.CharField(default='site', max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='handle',
            name='site',
        ),
        migrations.RemoveField(
            model_name='question_attachment',
            name='blog_key',
        ),
        migrations.RemoveField(
            model_name='support_attachment',
            name='blog_key',
        ),
        migrations.AlterField(
            model_name='handle',
            name='handle_id',
            field=models.CharField(default='handle', max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default='bf7f7f89-7a2c-446f-8c5c-83f6b2390b75', editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddField(
            model_name='handle',
            name='site_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.site'),
        ),
        migrations.AddField(
            model_name='question_attachment',
            name='blob_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob'),
        ),
        migrations.AddField(
            model_name='quiz_rendering',
            name='blob_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob'),
        ),
        migrations.AddField(
            model_name='support_attachment',
            name='blob_key',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mentapp.blob'),
        ),
    ]