# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction, connection

from scuelo.models import Classe

logger = logging.getLogger(__name__)


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
        except Exception as ex:
            logger.error('fixtures: %s' % str(ex))

    
