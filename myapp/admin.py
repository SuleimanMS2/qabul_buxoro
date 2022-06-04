from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from import_export import resources


# Register your models here.
class ResourceModel(resources.ModelResource):
    class Meta:
        model = Pasport
        fields = ('jshir', 'familiya', 'ism', 'sharif', 'tug_sana', 'millat_id__name', 'pass_kim_bergan_tuman_id__name',
                  'jins__name', 'pass_seriya', 'pass_raqam', 'pass_berilgan_sana', 'doimiy_viloyat__name',
                  'doimiy_tuman__name', 'doimiy_manzil', 'photo', 'telefon_raqam', 'telefon_raqam_2', 'talim_shakli',
                  'talim_yunalishi', 'diplom_raqam', 'diplom_file', 'harbiy_tavsiyanoma', 'ielts_sertifikat',
                  'davlat_mukofoti', 'davlat_mukofoti_pdf', 'qushulgan_sana', 'yangilangan_sana',)


@admin.register(Pasport)
class PassportAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ism', 'familiya', 'sharif', 'jshir',)
    list_display_links = ('ism', 'familiya', 'sharif', 'jshir')
    list_filter = ['qushulgan_sana', 'yangilangan_sana']
    search_fields = ('ism', 'familiya', 'sharif', 'jshir', 'pass_seriya', 'pass_raqam',)
    ordering = ['-id']
    exclude = ('random_son',)
    resource_class = ResourceModel
    # class Media:
    #     js = ('js/dropdown.js',)


class YonalishOTMAdmin(admin.ModelAdmin):
    list_filter = ['talim_shakli', 'talim_turi', ]
    search_fields = ('name',)


admin.site.register(Viloyat)
admin.site.register(Tuman)
admin.site.register(Millat)
admin.site.register(Jins)

admin.site.register(TalimShakli)
admin.site.register(TalimTili)
admin.site.register(TalimTuri)
admin.site.register(YonalishOTM, YonalishOTMAdmin)
admin.site.register(DavlatMukofoti)
admin.site.register(Ballar)
admin.site.register(Fanlar)

admin.site.index_title = 'Qabul 2022'
