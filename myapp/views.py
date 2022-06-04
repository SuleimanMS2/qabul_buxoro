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


class GeneratePdf(View):
    def get(self, request, pk, *args, **kwargs):
        talaba = Pasport.objects.filter(pk=pk)
        print(talaba.values()[0])

        ssilka = f'http://127.0.0.1:8000/pdf/{talaba.values()[0]["id"]}'
        img = qrcode.make(ssilka)
        img.save(f'static/qrcode/QRCode{talaba.values()[0]["id"]}.png')

        data = {
            'today': "talaba.values_list()[0]",
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'rasm': talaba.values()[0]["photo"],
            'qrcode': f'static/qrcode/MyQRCode{talaba.values()[0]["id"]}.png',
            'tuman': Tuman.objects.filter(pk=talaba.values()[0]["doimiy_tuman_id"]).values()[0]["name"],
        }
        pdf = render_to_pdf('invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
