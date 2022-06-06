from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse

from django.http import HttpResponse
from django.views.generic import View

from qabul_buxoro.utils import render_to_pdf
import qrcode

import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from telegram import Update
from django.views.decorators.csrf import csrf_exempt
from .qabul_bot.bot import bot, dispatcher


@method_decorator(csrf_exempt, 'dispatch')
class Master(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body)
            update: Update = Update.de_json(data, bot)
            dispatcher.process_update(update)
        except Exception as e:
            pass
        return HttpResponse('ok', status=200)


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
        uzb = str(pk)[:5]
        talaba = Pasport.objects.filter(pk=uzb)

        ballar = YonalishOTM.objects.filter(pk=talaba.values()[0]["talim_yunalishi_id"])
        print(ballar.values()[0])

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
        davlat_mukofoti = DavlatMukofoti.objects.filter(pk=talaba.values()[0]["davlat_mukofoti_id"])

        # print(davlat_mukofoti, 'ashdbjsadbjdbhdbjda')
        def sonlar(son):
            if son:
                return son.values()[0]["name"]
            else:
                return "---"

        def func_ball(bal):
            if bal:
                return bal
            else:
                return "---"

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
            'davlat_mukofoti': sonlar(davlat_mukofoti),
            'talim_shakli_turi': f'{talim_shakli}, {talim_turi}',
            'talim_yunalishi': talim_yunalishi,
            'qushulgan_sana': f'{talaba.values()[0]["tug_sana"]}',

            'photo': talaba.values()[0]["photo"],
            'qrcode': f'static/qrcode/QRCode{talaba.values()[0]["id"]}.png',

            'fan_1': sonlar(Fanlar.objects.filter(pk=ballar.values()[0]["fan_name_1_id"])),
            'fan_2': sonlar(Fanlar.objects.filter(pk=ballar.values()[0]["fan_name_2_id"])),
            'fan_3': sonlar(Fanlar.objects.filter(pk=ballar.values()[0]["fan_name_3_id"])),
            'fan_4': sonlar(Fanlar.objects.filter(pk=ballar.values()[0]["fan_name_4_id"])),
            'fan_5': sonlar(Fanlar.objects.filter(pk=ballar.values()[0]["fan_name_5_id"])),

            'ball_1': sonlar(Ballar.objects.filter(pk=ballar.values()[0]["fan_ball_1_id"])),
            'ball_2': sonlar(Ballar.objects.filter(pk=ballar.values()[0]["fan_ball_2_id"])),
            'ball_3': sonlar(Ballar.objects.filter(pk=ballar.values()[0]["fan_ball_3_id"])),
            'ball_4': sonlar(Ballar.objects.filter(pk=ballar.values()[0]["fan_ball_4_id"])),
            'ball_5': sonlar(Ballar.objects.filter(pk=ballar.values()[0]["fan_ball_5_id"])),

            'savol_son1': func_ball(ballar.values()[0]["savol_soni_1"]),
            'savol_son2': func_ball(ballar.values()[0]["savol_soni_2"]),
            'savol_son3': func_ball(ballar.values()[0]["savol_soni_3"]),
            'savol_son4': func_ball(ballar.values()[0]["savol_soni_4"]),
            'savol_son5': func_ball(ballar.values()[0]["savol_soni_5"]),
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
