from django.contrib import admin
from .models import  Eleve , Classe, Inscription, AnneeScolaire
from django.contrib import admin



class SicAdminArea(admin.AdminSite):
    site_header = 'SICS NASSARA'
    site_title = 'SICS NASSARA'
    index_title = 'SICS NASSARA'


sics_site = SicAdminArea(name='SICS NASSARA')



class  ClasseAdmin(admin.ModelAdmin):
    
    list_display = ['type_ecole'  ,  'nom']


class AnneeScolaireInline(admin.TabularInline):
    model = AnneeScolaire
    
class ClasseInline(admin.TabularInline):
    model =  Classe 
    
class EleveInline(admin.TabularInline):
    model =  Eleve
    

class  InscriptionInline(admin.TabularInline):
    model = Inscription
    
    inlines = [ EleveInline, ClasseInline, AnneeScolaireInline ]

sics_site.register(Eleve)
sics_site.register(AnneeScolaire)
sics_site.register(Inscription)
sics_site.register(Classe ,ClasseAdmin )
'''
class EleveAdmin(admin.ModelAdmin):
    fieldsets = (
        ('INFORMATIONS DE  BASE', {
            'fields': ('nom', 'prenom', 'sex',
                       'date_naissance'
            ),
        }
         ),
        ('INFORMATION   CLASSE', {
            'fields': ('type_ecole', 'nom_classe'
                       ,'annee_inscr'),
        }
         ),
        ('INFORMATION SOCIALE', {
            'fields': ('condition_eleve', 'cs_py' ,'hand'
                       ,'date_enquete'),
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
        'sex','type_ecole', 'nom_classe'
    ]
    
    jazzmin_section_order = ('nom_class')
    #list_select_related =
    search_fields = ['nom', 'prenom']
    list_filter = ['nom_classe']
    ordering= ["nom_classe"]
    #list_select_related = ['paiment_set']
    #list_select_related = ['paiement_set']
    # Add 'nom_classe' to filter by class
   # inlines =[PaimentInline ,]
    
    def __str__( self ):
        return self.name'''
   



#admin.site.register(Eleve, EleveAdmin)
#admin.site.site_header = 'SICS NASSARA'
#admin.site.site_title = 'SICS NASSARA'
#admin.site.index_title = 'SICS NASSARA'


#admin.site. = 'Admin Customization'