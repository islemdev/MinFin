import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from polls.models import Citoyen, Infraction

# Create your views here.
def show(request, cin):
    data = Citoyen.objects.filter(cin=int(cin)).values('nom', 'prenom', 'email')

    if not data:
        return JsonResponse({'code': 0, 'message': 'numero de carte inexistant'}, safe=False)
    else:
        test = Infraction.objects.filter(cin_citoyen=int(cin))
        infraction = Infraction.objects.filter(cin_citoyen=int(cin)).values('date_creation', 'montant', 'etat_paiement')
        if test:
            return JsonResponse({'code': 1, 'citoyen': list(data),
            'infraction': list(infraction)}, safe=False)
        else:
            return JsonResponse({'code': 1, 'citoyen': list(data), 'Information': "aucune infraction"}, safe=False)

@csrf_exempt
def insertCitoyen(request):
        citoyens=[{"cin":12345678,"nom":"Bedhief","prenom":"Youssef","email":"youssefbedhief@gmail.com"},
                  {"cin":12356987,"nom":"Bouriga","prenom":"Yosra","email":"yosrabouriga@gmail.com"},
                  {"cin":11111111,"nom":"Hajji","prenom":"Yassine","email":"yassinehajji@gmail.com"},
                  {"cin":98765421,"nom":"Frioui","prenom":"Islem","email":"islemfrioui@gmail.com"}]
        for c in citoyens:
            citoyenInserted = Citoyen(cin=c["cin"], nom=c["nom"], prenom=c["prenom"], email=c["email"])
            citoyenInserted.save()
        return JsonResponse({'code': 1})

@csrf_exempt
def insertInfraction(request):
    infractions = [{"cin": 12345678, "montant": 250, "etat_paiement": 1},
                {"cin": 12356987, "montant": 100, "etat_paiement": 1},
                {"cin": 11111111, "montant": 60, "etat_paiement": 0}]

    for i in infractions:
           infractionInserted = Infraction(cin_citoyen=Citoyen.objects.get(cin=i["cin"]), date_creation=datetime.datetime.now(), montant=i["montant"], etat_paiement=i["etat_paiement"])
           infractionInserted.save()
    return JsonResponse({'code': 1})
