# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Citoyen(models.Model):
    cin = models.IntegerField(db_column='CIN', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=255)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'citoyen'


class Infraction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cin_citoyen = models.ForeignKey(Citoyen, models.DO_NOTHING, db_column='cin_citoyen')
    date_creation = models.DateField()
    montant = models.FloatField()
    etat_paiement = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'infraction'
