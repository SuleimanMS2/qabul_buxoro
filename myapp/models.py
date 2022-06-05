from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.html import format_html

# Create your models here.
from django.utils.safestring import mark_safe
from smart_selects.db_fields import ChainedForeignKey
import random


def validate_image(image):
    filesize = image.file.size
    max_height = 480
    max_width = 360
    height = image.height
    width = image.width
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Maks. fayl hajmi %sMB" % str(megabyte_limit))
    if width > max_width or height > max_height:
        raise ValidationError("Fayl o`lchami ruxsat etilganidan kattaroq (3X4)")


def validate_file(fieldss):
    filesize = fieldss.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Maks. fayl hajmi %sMB" % str(megabyte_limit))


class Viloyat(models.Model):
    """Viloyat"""
    name = models.CharField("Viloyat", max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Viloyat "
        verbose_name_plural = "Viloyatlar"


'''o'tgan'''


class Tuman(models.Model):
    """Tuman"""
    name = models.CharField("Tuman", max_length=60)
    viloyat = models.ForeignKey(Viloyat, verbose_name="viloyat", on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tuman "
        verbose_name_plural = "Tumanlar"


class Millat(models.Model):
    """ Millat """
    name = models.CharField(verbose_name="Millati", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Millat "
        verbose_name_plural = "Millatlar"


class Jins(models.Model):
    """ Jins """
    name = models.CharField(verbose_name="Jinsi", max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Jins "
        verbose_name_plural = "Jinslar"


class Pasport(models.Model):
    """ Fuqaro """

    reg_message = 'Ma`lumot xato kiritildi!'  # Validator message
    phone_regex = RegexValidator(regex=r'^[0-9]{9}', message=reg_message)  # Telefon raqam validator
    jshir_regax = RegexValidator(regex=r'^[0-9]{14}', message=reg_message)  # JSHshir validator
    pass_regax = RegexValidator(regex=r'^[0-9]{7}', message=reg_message)  # Pasport seriya validator

    jshir = models.CharField(verbose_name="JSHIR", validators=[jshir_regax], unique=True, max_length=14)
    familiya = models.CharField(max_length=30)
    ism = models.CharField(max_length=30)
    sharif = models.CharField(max_length=30)
    tug_sana = models.DateField()
    millat_id = models.ForeignKey(Millat, verbose_name="Millat", on_delete=models.PROTECT, related_name='millat')
    pass_kim_bergan_tuman_id = models.ForeignKey(Tuman, verbose_name="Passport bergan tuman", related_name='+',
                                                 on_delete=models.PROTECT)
    jins = models.ForeignKey(Jins, verbose_name="Jinsi", on_delete=models.PROTECT, related_name='jins')
    pass_seriya = models.CharField(max_length=2, verbose_name="Passport seriyasi")
    pass_raqam = models.CharField(verbose_name="Passport raqami", max_length=7, validators=[pass_regax])
    pass_berilgan_sana = models.DateField()
    doimiy_viloyat = models.ForeignKey(Viloyat, verbose_name="Doimiy yashash viloyati", on_delete=models.PROTECT)
    doimiy_tuman = ChainedForeignKey(Tuman, verbose_name="Doimiy yashash tumani", on_delete=models.PROTECT,
                                     chained_field="doimiy_viloyat",
                                     chained_model_field="viloyat",
                                     show_all=False,
                                     auto_choose=True,
                                     sort=True)
    doimiy_manzil = models.CharField(max_length=250, verbose_name="Doimiy yashash manzili", blank=True, null=True,
                                     help_text='Obod ko`cha 5-uy')
    photo = models.ImageField(upload_to='static/talaba/', verbose_name="Abituriyent rasmi", validators=[validate_image],
                              help_text='Maksimum fayl hajmi 2Mb')
    telefon_raqam = models.CharField(validators=[phone_regex], max_length=9, help_text='Telegram raqam (93)123-45-67')
    telefon_raqam_2 = models.CharField(validators=[phone_regex], max_length=9, null=True, blank=True,
                                       verbose_name='Qo`shimcha raqam',
                                       help_text='Qoshimcha raqam, Majburiy emas', )
    talim_turi = models.ForeignKey('TalimTuri', on_delete=models.PROTECT, verbose_name='Ta`lim turi')
    talim_shakli = models.ForeignKey('TalimShakli', on_delete=models.PROTECT, verbose_name='Ta`lim shakli')
    talim_yunalishi = ChainedForeignKey('YonalishOTM', on_delete=models.PROTECT, verbose_name='OTM Yo`nalishi',
                                        chained_field="talim_shakli",
                                        chained_model_field="talim_shakli",
                                        show_all=False,
                                        auto_choose=True,
                                        sort=True)

    diplom_raqam = models.CharField(max_length=30, verbose_name='Diplom raqami')
    diplom_file = models.FileField(upload_to='static/diplom/', verbose_name='Diplom/Shahodatnoma fayl', blank=True,
                                   null=True, validators=[validate_file], help_text='PDF-Rasm file maks. 5MB')

    harbiy_tavsiyanoma = models.FileField(upload_to='static/harbiy/', verbose_name='Harbiy tavsiyanoma', blank=True,
                                          null=True, validators=[validate_file], help_text='PDF-Rasm file maks. 5MB')
    ielts_sertifikat = models.ImageField(upload_to='static/ielts/', verbose_name='IELTS sertifikati', null=True,
                                         blank=True, validators=[validate_file], help_text='Rasm maks. 5MB')
    davlat_mukofoti = models.ForeignKey('DavlatMukofoti', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Davlat mukofoti', default='Null')
    davlat_mukofoti_pdf = models.FileField(upload_to='static/d_mukofot/', validators=[validate_file],
                                           verbose_name='Davlat mukofoti pdf shakli', null=True, blank=True,
                                           help_text='PDF-Rasm file maks. 5 MB')

    random_son = models.BigIntegerField(default=random.randrange(1000000, 9999999))
    qushulgan_sana = models.DateTimeField(auto_now_add=True, verbose_name='Qo`shilgan sana')
    yangilangan_sana = models.DateTimeField(auto_now=True, verbose_name='Yangilangan sana')

    def __str__(self):
        return self.familiya

    def Chop_Etish(self):
        a = str(self.id) + str(self.random_son)
        return mark_safe(
            f'<a href="http://52.73.249.232/pdf/{a}" target="_blank">Chop Etish</a>')

    class Meta:
        verbose_name = "Hujjat qabul qilish "
        verbose_name_plural = "Hujjat qabul qilish "


class TalimTuri(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ta`lim Turi')
    talim_shakllari = models.ManyToManyField('TalimShakli', verbose_name='Talim Shakli', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ta`lim Turi '
        verbose_name_plural = 'Ta`lim Turlari'


class TalimShakli(models.Model):
    """ Talim Shakli """
    name = models.CharField(max_length=50, verbose_name='Ta`lim shakli')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ta`lim Shakli '
        verbose_name_plural = 'Ta`lim Shakllari'


class TalimTili(models.Model):
    """ Til """
    name = models.CharField(max_length=50, verbose_name='Ta`lim Tili')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ta`lim Tili '
        verbose_name_plural = 'Ta`lim Tillari'


class YonalishOTM(models.Model):
    """ Yo`nalish nomi """
    name = models.CharField(max_length=255, verbose_name='OTM yo`nalish nomi')
    talim_tili = models.ForeignKey(TalimTili, on_delete=models.PROTECT, verbose_name='Ta`lim tili')
    talim_shakli = models.ForeignKey(TalimShakli, on_delete=models.PROTECT, verbose_name='Ta`lim Shakli')
    talim_turi = models.ForeignKey(TalimTuri, on_delete=models.PROTECT, verbose_name='Ta`lim turi')
    fan_name_1 = models.ForeignKey('Fanlar', on_delete=models.PROTECT, verbose_name='Fan-1', null=True, blank=True,
                                   default='Null')
    fan_ball_1 = models.ForeignKey('Ballar', on_delete=models.PROTECT, verbose_name='Ball-1', null=True, blank=True,
                                   default='Null')
    savol_soni_1 = models.SmallIntegerField(verbose_name='Savol soni-1', null=True, blank=True)
    fan_name_2 = models.ForeignKey('Fanlar', on_delete=models.PROTECT, verbose_name='Fan-2', null=True, blank=True,
                                   related_name='+', default='Null')
    fan_ball_2 = models.ForeignKey('Ballar', on_delete=models.PROTECT, verbose_name='Ball-2', null=True, blank=True,
                                   related_name='+', default='Null')
    savol_soni_2 = models.SmallIntegerField(verbose_name='Savol soni-2', null=True, blank=True, default='Null')

    fan_name_3 = models.ForeignKey('Fanlar', on_delete=models.PROTECT, verbose_name='Fan-3', null=True, blank=True,
                                   related_name='+', default='Null')
    fan_ball_3 = models.ForeignKey('Ballar', on_delete=models.PROTECT, verbose_name='Ball-3', null=True, blank=True,
                                   related_name='+', default='Null')
    savol_soni_3 = models.SmallIntegerField(verbose_name='Savol soni-3', null=True, blank=True, default='Null')

    fan_name_4 = models.ForeignKey('Fanlar', on_delete=models.PROTECT, verbose_name='Fan-4', null=True, blank=True,
                                   related_name='+', default='Null')
    fan_ball_4 = models.ForeignKey('Ballar', on_delete=models.PROTECT, verbose_name='Ball-4', null=True, blank=True,
                                   related_name='+', default='Null')
    savol_soni_4 = models.SmallIntegerField(verbose_name='Savol soni-4', null=True, blank=True, default='Null')

    fan_name_5 = models.ForeignKey('Fanlar', on_delete=models.PROTECT, verbose_name='Fan-5', null=True, blank=True,
                                   related_name='+', default='Null')
    fan_ball_5 = models.ForeignKey('Ballar', on_delete=models.PROTECT, verbose_name='Ball-5', null=True, blank=True,
                                   related_name='+', default='Null')
    savol_soni_5 = models.SmallIntegerField(verbose_name='Savol soni-5', null=True, blank=True, default='Null')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'OTM Yo`nalish '
        verbose_name_plural = 'OTM Yo`nalishlar'


class DavlatMukofoti(models.Model):
    """ Davlat mukofoti """
    name = models.CharField(max_length=255, verbose_name='Davlat mukofoti')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Davlat mukofoti '
        verbose_name_plural = 'Davlat mukofotlari'


class Fanlar(models.Model):
    name = models.CharField(max_length=100, verbose_name='Fan nomi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fan '
        verbose_name_plural = 'Fanlar '


class Ballar(models.Model):
    name = models.DecimalField(verbose_name='Ballar', max_digits=2, decimal_places=1)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Ball '
        verbose_name_plural = 'Ballar '
