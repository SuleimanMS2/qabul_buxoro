# Generated by Django 3.0 on 2022-06-04 16:33

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_ballar_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ballar',
            name='photo',
        ),
        migrations.AddField(
            model_name='pasport',
            name='random_son',
            field=models.BigIntegerField(default=5260012),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='davlat_mukofoti_pdf',
            field=models.FileField(blank=True, help_text='PDF-Rasm file maks. 5 MB', null=True, upload_to='static/d_mukofot/', validators=[myapp.models.validate_file], verbose_name='Davlat mukofoti pdf shakli'),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='diplom_file',
            field=models.FileField(blank=True, help_text='PDF-Rasm file maks. 5MB', null=True, upload_to='static/diplom/', validators=[myapp.models.validate_file], verbose_name='Diplom/Shahodatnoma fayl'),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='harbiy_tavsiyanoma',
            field=models.FileField(blank=True, help_text='PDF-Rasm file maks. 5MB', null=True, upload_to='static/harbiy/', validators=[myapp.models.validate_file], verbose_name='Harbiy tavsiyanoma'),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='ielts_sertifikat',
            field=models.ImageField(blank=True, help_text='Rasm maks. 5MB', null=True, upload_to='static/ielts/', validators=[myapp.models.validate_image], verbose_name='IELTS sertifikati'),
        ),
        migrations.AlterField(
            model_name='pasport',
            name='photo',
            field=models.ImageField(help_text='Maksimum fayl hajmi 2Mb', upload_to='static/talaba/', validators=[myapp.models.validate_image], verbose_name='Rasm'),
        ),
    ]