import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pika
from polls.models import Citoyen, Infraction
import json


# Create your views here.
def show(request, cin):
    print("sdgsdg")
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='queue_logger', durable=True)

    data = Citoyen.objects.filter(cin=int(cin)).values('nom', 'prenom', 'email')
    if not data:
        response_data = {'code': 0, 'message': 'numero de carte inexistant'}
        response = JsonResponse(response_data, safe=False)
        print(type(response))
        response['Access-Control-Allow-Origin'] = '*'
        response['Content-Type'] = 'application/json'
        channel.basic_publish(exchange='', routing_key='queue_logger', body=json.dumps({'cin': cin, 'response': response_data}),
                              properties=pika.BasicProperties(
                                  content_type='application/json',
                                  delivery_mode=2  # make messages persistent
                              ))
        connection.close()
        return response
    else:
        test = Infraction.objects.filter(cin_citoyen=int(cin))
        infraction = Infraction.objects.filter(cin_citoyen=int(cin)).values('date_creation', 'montant', 'etat_paiement')
        if test:
            response_data = {'code': 1, 'citoyen': list(data),
            'infraction': list(infraction)}
            response = JsonResponse(response_data, safe=False)
            response['Access-Control-Allow-Origin'] = '*'
            response['Content-Type'] = 'application/json'
            channel.basic_publish(exchange='', routing_key='queue_logger',
                                  body=json.dumps({'cin': cin, 'response': response_data}),
                                  properties=pika.BasicProperties(
                                      content_type='text/plain',
                                      delivery_mode=2  # make messages persistent
                                  ))
            connection.close()
            return response
        else:
            response_data= {'code': 1, 'citoyen': list(data), 'Information': "aucune infraction"}
            response = JsonResponse(response_data, safe=False)
            response['Access-Control-Allow-Origin'] = '*'
            response['Content-Type'] = 'application/json'
            channel.basic_publish(exchange='', routing_key='queue_logger',
                                  body=json.dumps({'cin': cin, 'response': response_data}),
                                  properties=pika.BasicProperties(
                                      content_type='text/plain',
                                      delivery_mode=2  # make messages persistent
                                  ))
            connection.close()
            return response

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
