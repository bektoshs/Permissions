# Generated by Django 4.2.10 on 2024-07-18 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0011_userpermission_object_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermission',
            name='basis_given_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bases_given_by', to=settings.AUTH_USER_MODEL),
        ),
    ]