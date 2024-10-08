# Generated by Django 5.0.6 on 2024-06-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storages', '0003_alter_storage_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='host',
            field=models.CharField(help_text='Enter host.', verbose_name='host'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='vendor',
            field=models.CharField(choices=[('postgresql', 'PostgreSQL'), ('mysql', 'MySQL')], verbose_name='vendor'),
        ),
    ]
