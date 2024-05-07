# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User, Permission
from django.conf import settings
from django.db import transaction, connection

from scuelo.models import Classe

logger = logging.getLogger(__name__)


def attribuer_tous_autorisations(groups, modelli):
    if not type(groups) is list:
        groups = [groups]
    for group in groups:
        for permesso in modelli:
            for p in Permission.objects.filter(content_type__app_label=permesso['app_label'],
                                               content_type__model=permesso['model']):
                if p not in group.permissions.all():
                    group.permissions.add(p)


class Command(BaseCommand):
    help = '''Inserts class data'''

    def handle(self, *args, **options):
        try:
            Classe.objects.get_or_create(type_ecole='M', nom='PS')
            Classe.objects.get_or_create(type_ecole='M', nom='MS')
            Classe.objects.get_or_create(type_ecole='M', nom='GS')
            Classe.objects.get_or_create(type_ecole='P', nom='CP1')
            Classe.objects.get_or_create(type_ecole='P', nom='CP2')
            Classe.objects.get_or_create(type_ecole='P', nom='CE1')
            Classe.objects.get_or_create(type_ecole='P', nom='CE2')
            Classe.objects.get_or_create(type_ecole='P', nom='CM1')
            Classe.objects.get_or_create(type_ecole='P', nom='CM2')
            gr_operateur, _ = Group.objects.get_or_create(name='Opérateur')
            superuser, _ = User.objects.get_or_create(username='superuser',
                                                   first_name='Super',
                                                   last_name='User',
                                                   is_superuser=True,
                                                   is_staff=True,
                                                   email='davide@c4k.it')
            superuser.set_password('superuser')
            superuser.save()
            operateur, _ = User.objects.get_or_create(username='operateur',
                                                   first_name='Operateur',
                                                   last_name='Sics Nassara',
                                                   is_staff=True,
                                                   email='davide@c4k.it')
            operateur.set_password('operateur')
            operateur.groups.add(gr_operateur)
            operateur.save()
            modelli_autorisations_complet = [
                {'app_label': 'scuelo', 'model': 'classe'},
                {'app_label': 'scuelo', 'model': 'eleve'},
                {'app_label': 'scuelo', 'model': 'anneescolaire'},
                {'app_label': 'scuelo', 'model': 'inscription'},
                {'app_label': 'scuelo', 'model': 'paiement'}
            ]
            groupes_autorisations_complet = [
                gr_operateur
            ]
            attribuer_tous_autorisations(groupes_autorisations_complet, modelli_autorisations_complet)

        except Exception as ex:
            logger.error('fixtures: %s' % str(ex))
