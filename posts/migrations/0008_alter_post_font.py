# Generated by Django 4.0 on 2022-03-16 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_font_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='font',
            field=models.IntegerField(blank=True, choices=[(1, 'Noto Serif SC'), (2, 'EB Garamond'), (3, 'Shippori Mincho')], null=True),
        ),
    ]
