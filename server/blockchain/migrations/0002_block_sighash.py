# Generated by Django 2.2.1 on 2019-05-27 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='sighash',
            field=models.CharField(default='', max_length=64),
        ),
    ]
