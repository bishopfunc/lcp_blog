# Generated by Django 4.0 on 2022-03-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_draft_flg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='draft_flg',
            field=models.BooleanField(default=False, verbose_name='下書きで保存'),
        ),
    ]
