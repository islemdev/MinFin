from django.http import JsonResponse
from django.shortcuts import render
from polls.models import Citoyen
from django.core import serializers

# Create your views here.

def show(request, cin):
    # citoyen = Citoyen.objects.all()
  #  data = serializers.serialize("json", Citoyen.objects.filter(cin=int(cin)))
    data = Citoyen.objects.filter(cin=int(cin))

    if not data and False:
        return JsonResponse({'code':0, 'msg':'laylay'}, safe=False)
    if False:
        return JsonResponse({'code':1, 'citoyen':{
            'nom':'Frioui',
            'prenom':'Islem'
        },
        'etat':0}, safe=False)
    if True:
        return JsonResponse({'code': 1, 'citoyen': {
            'nom': 'Frioui',
            'prenom': 'Islem'
        },
        'etat': 1,
        'liste':[{}]}, safe=False)



    print("les informations du citoyen de num cin : \n", cin)
    print(data)
    return JsonResponse(data, safe=False)

