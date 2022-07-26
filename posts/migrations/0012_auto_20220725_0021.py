# Generated by Django 3.2.6 on 2022-07-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20220724_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts', to='posts.Tag', verbose_name='Tag'),
        ),
        migrations.AlterField(
            model_name='category',
            name='text',
            field=models.CharField(blank=True, max_length=100, verbose_name='説明'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='text',
            field=models.CharField(blank=True, max_length=100, verbose_name='説明'),
        ),
    ]