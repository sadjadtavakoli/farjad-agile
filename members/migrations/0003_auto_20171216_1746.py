# Generated by Django 2.0rc1 on 2017-12-16 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='age',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
    ]