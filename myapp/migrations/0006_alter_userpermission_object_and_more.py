# Generated by Django 4.2.10 on 2024-07-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_userpermission_object_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermission',
            name='object',
            field=models.CharField(choices=[('os', 'Os'), ('host', 'Host'), ('backend', 'Backend'), ('user', 'User'), ('frontend', 'Front'), ('hardware', 'Hardware'), ('database', 'DataBase'), ('at', 'AT')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userpermission',
            name='subject',
            field=models.CharField(choices=[('os', 'Os'), ('host', 'Host'), ('backend', 'Backend'), ('user', 'User'), ('frontend', 'Front'), ('hardware', 'Hardware'), ('database', 'DataBase'), ('at', 'AT')], max_length=50),
        ),
    ]