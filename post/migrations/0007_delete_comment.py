# Generated by Django 4.0.3 on 2022-05-30 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]