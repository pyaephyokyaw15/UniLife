# Generated by Django 4.0.3 on 2022-04-30 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_banner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='date_posted',
            new_name='created_date',
        ),
        migrations.RemoveField(
            model_name='post',
            name='banner',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
