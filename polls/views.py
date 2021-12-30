
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

#Link : http://localhost:8000/polls/insertCitoyen?cin=12345678&nom=Bedhief&prenom=Youssef&email=youssefbedhief@gmail.com
#Link : http://localhost:8000/polls/insertCitoyen?cin=12356987&nom=Bouriga&prenom=Yosra&email=yosrabouriga@gmail.com
#Link : http://localhost:8000/polls/insertCitoyen?cin=11111111&nom=Hajji&prenom=Yassine&email=yassinehajji@gmail.com
#Link : http://localhost:8000/polls/insertCitoyen?cin=98765421&nom=Frioui&prenom=Islem&email=islemfrioui@gmail.com

@csrf_exempt
def insertCitoyen(request):
    if (request.method == "GET"):
        cin=request.GET.get('cin')
        nom=request.GET.get('nom')
        prenom=request.GET.get('prenom')
        email=request.GET.get('email')

        citoyenInserted = Citoyen(cin=int(cin), nom=nom, prenom=prenom, email=email)
        citoyenInserted.save()
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'msg': 'no'})

#http://localhost:8000/polls/insertInfraction?cin_citoyen=11111111&date_creation=2021-10-10&montant=60&etat_paiement=1
#http://localhost:8000/polls/insertInfraction?cin_citoyen=12345678&date_creation=2021-12-29&montant=250&etat_paiement=1
#http://localhost:8000/polls/insertInfraction?cin_citoyen=12356987&date_creation=2021-10-28&montant=100&etat_paiement=0

@csrf_exempt
def insertInfraction(request):
    if (request.method == "GET"):
        cin = request.GET.get('cin_citoyen')
        date_creation = request.GET.get('date_creation')
        montant = request.GET.get('montant')
        etat_paiement = request.GET.get('etat_paiement')

        infractionInserted = Infraction(cin_citoyen=Citoyen.objects.get(cin=int(cin)), date_creation=date_creation, montant=montant, etat_paiement=etat_paiement)
        infractionInserted.save()
        return JsonResponse({'code': 1})
    else:
        return JsonResponse({'msg': 'no'})