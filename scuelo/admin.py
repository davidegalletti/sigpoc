from django.contrib import admin
from .models import Classe, Eleve, AnneeScolaire, Inscription, Paiement
from django.contrib.auth.models import User, Group


class SicAdminArea(admin.AdminSite):
    site_header = 'SICS NASSARA'
    site_title = 'SICS NASSARA'
    index_title = 'SICS NASSARA'


sics_site = SicAdminArea(name='SICS NASSARA')


class PaimentInline(admin.TabularInline):
    model = Paiement
    '''raw_id_fields = ['causal', 'montant',
                    'date_paiement',
                    'note_paiement']
    '''


class EleveAdmin(admin.ModelAdmin):
    fieldsets = (
        ('INFORMATIONS DE  BASE', {
            'fields': ('nom', 'prenom', 'sex',
                       'date_naissance'
                       ),
        }
         ),
        ('INFORMATION SOCIALE', {
            'fields': ('condition_eleve', 'cs_py', 'hand'
                       , 'date_enquete'),
        }
         ),
        ('INFORMATION PARENT', {
            'fields': ('parent', 'tel_parent',
                       ),
        }
         )
    )

    list_display = [
        'nom', 'prenom', 'condition_eleve',
        'sex'
    ]

    jazzmin_section_order = 'nom_class'
    # list_select_related =
    search_fields = ['nom', 'prenom']
    # list_filter = ['nom_classe']
    # ordering = ["nom_classe"]
    # list_select_related = ['paiment_set']
    # list_select_related = ['paiement_set']
    # Add 'nom_classe' to filter by class
    inlines = [PaimentInline, ]


class PaiementAdmin(admin.ModelAdmin):
    list_display = [
        'causal', 'montant',
        'date_paiement', 'note_paiement'
    ]
    # filter_horizontal = True

    list_select_related = ["eleve_payment"]
    # inlines = [ EleveInline ,]
    # readonly_fields = ["elevepayment"]

    '''def get_list_display(self, request):
        # Add 'section' to list_display
        return super().get_list_display(request) + ['section']

    def section(self, obj):
        # Custom method to display the class section
        return obj.nom_classe

    section.admin_order_field = 'nom_classe'  # Enable sorting by section

    def get_list_display_links(self, request, list_display):
        # Disable editing links for 'section' column
        return ['nom_classe']
        '''


class InscriptionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['eleve']



sics_site.register(Paiement, PaiementAdmin)
sics_site.register(Eleve, EleveAdmin)
sics_site.register(Classe)
sics_site.register(AnneeScolaire)
sics_site.register(Inscription, InscriptionAdmin)
sics_site.register(User)
sics_site.register(Group)
