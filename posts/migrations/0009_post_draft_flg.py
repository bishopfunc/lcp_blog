# Generated by Django 4.0 on 2022-03-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_font'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft_flg',
            field=models.BooleanField(default=True),
        ),
    ]
