from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse


class ViloyatList(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        viloyat = request.data['viloyat']
        tuman = {}
        if viloyat:
            tumanlar = Viloyat.objects.get(id=viloyat).viloyat_id.all()
            tuman = {p.name: p.id for p in tumanlar}
        return JsonResponse(data=tuman, safe=False)
