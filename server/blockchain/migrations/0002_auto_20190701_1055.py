# Generated by Django 2.2.1 on 2019-07-01 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='hash',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='block',
            name='prevhash',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='block',
            name='status',
            field=models.BooleanField(),
        ),
    ]
