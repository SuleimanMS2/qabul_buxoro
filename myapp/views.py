from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse

from django.http import HttpResponse
from django.views.generic import View

from qabul_buxoro.utils import render_to_pdf
import qrcode


class ViloyatList(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        viloyat = request.data['viloyat']
        tuman = {}
        if viloyat:
            tumanlar = Viloyat.objects.get(id=viloyat).viloyat_id.all()
            tuman = {p.name: p.id for p in tumanlar}
        return JsonResponse(data=tuman, safe=False)


def photo_control(image):
    if image == '':
        return "Yo`q"
    else:
        return "Bor"


class GeneratePdf(View):
    def get(self, request, pk, *args, **kwargs):
        talaba = Pasport.objects.filter(pk=pk)
        print(talaba.values()[0])

        ssilka = f'http://127.0.0.1:8000/pdf/{talaba.values()[0]["id"]}'
        img = qrcode.make(ssilka)
        img.save(f'static/qrcode/QRCode{talaba.values()[0]["id"]}.png')

        millat = Millat.objects.filter(pk=talaba.values()[0]["millat_id_id"]).values()[0]["name"]
        jins = Jins.objects.filter(pk=talaba.values()[0]["jins_id"]).values()[0]["name"]
        viloyat = Viloyat.objects.filter(pk=talaba.values()[0]["doimiy_viloyat_id"]).values()[0]["name"]
        tuman = Tuman.objects.filter(pk=talaba.values()[0]["doimiy_tuman_id"]).values()[0]["name"]
        talim_shakli = TalimShakli.objects.filter(pk=talaba.values()[0]["talim_shakli_id"]).values()[0]["name"]
        talim_turi = TalimTuri.objects.filter(pk=talaba.values()[0]["talim_turi_id"]).values()[0]["name"]
        talim_yunalishi = YonalishOTM.objects.filter(pk=talaba.values()[0]["talim_yunalishi_id"]).values()[0]["name"]


        data = {
            'id': talaba.values()[0]["id"],
            'jshir': talaba.values()[0]["jshir"],
            'familiya': talaba.values()[0]["familiya"],
            'ism': talaba.values()[0]["ism"],
            'sharif': talaba.values()[0]["sharif"],
            'tug_sana': f'{talaba.values()[0]["tug_sana"]}',
            'millat_id': millat,
            'jins_id': jins,
            'pass_seriya_raqam': f'{talaba.values()[0]["pass_seriya"]} {talaba.values()[0]["pass_raqam"]}',
            'doimiy_manzil': f'{viloyat}, {tuman}, {talaba.values()[0]["doimiy_manzil"]}',
            'telegram_raqam': f'+998 {talaba.values()[0]["telefon_raqam"]}',
            'diplom_raqam': talaba.values()[0]["diplom_raqam"],
            'ielts_sertifikat': photo_control(talaba.values()[0]["ielts_sertifikat"]),
            'davlat_mukofoti': photo_control(talaba.values()[0]["davlat_mukofoti_id"]),
            'talim_shakli_turi': f'{talim_shakli}, {talim_turi}',
            'talim_yunalishi': talim_yunalishi,

            'photo': talaba.values()[0]["photo"],
            'qrcode': f'static/qrcode/QRCode{talaba.values()[0]["id"]}.png',
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

#  'photo': 'static/talaba/3x4.jpeg',

#  'harbiy_tavsiyanoma': 'static/harbiy/Screenshot_from_2022-06-01_10-11-07.png',

