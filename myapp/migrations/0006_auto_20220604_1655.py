# Generated by Django 3.0 on 2022-06-04 16:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20220604_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasport',
            name='random_son',
            field=models.BigIntegerField(default=8031036),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='telefon_raqam',
            field=models.CharField(help_text='Telegram raqam (93)123-45-67', max_length=9, validators=[django.core.validators.RegexValidator(message='Ma`lumot xato kiritildi!', regex='^[0-9]{9}')]),
        ),
    ]
