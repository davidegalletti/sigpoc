import  os
import  django
import pandas as pd
from scuelo.models import Paiement , Eleve , Classe


# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scuelo.settings')
django.setup()
xlpath = 'scuelo/dataloadprocess/Export SICS 2.1.75 (1).xlsx'

# Read Excel data into DataFrames
paiement_data = pd.read_excel(xlpath, sheet_name='Paiement')
eleve_data = pd.read_excel(xlpath, sheet_name='Eleve')
classe_data = pd.read_excel(xlpath, sheet_name='Classe')
# Import data into Paiement model
for _, row in paiement_data.iterrows():
    paiement = Paiement.objects.create(
        causal=row['_PK_Paiement_ID'],
        montant=row['__FK_Eleve'],
        date=row['Date_paiement'],
        note=row['Note_Paiement']
        # Add other fields as needed
    )

# Import data into Eleve model
for _, row in eleve_data.iterrows():
    eleve = Eleve.objects.create(
        nom=row['Nom'],
        prenom=row['Prenom'],
        date_enquete=row['D_enquete'],
        condition_eleve=row['Condition_eleve'],
        sex=row['Sex'],
        date_naissance=row['Date-Naissance'],
        cs_py=row['CS_PY'],
        hand=row['Hand'],
        annee_inscr=row['A_inscr'],
        parent=row['Parent'],
        tel_parent=row['Tel_parent']
        # Add other fields as needed
    )

# Import data into Classe model
for _, row in classe_data.iterrows():
    classe = Classe.objects.create(
        nom=row['Nom_Classe'],
        type_ecole=row['Type_Ecole'],
        ordre_classe=row['Ordre_Classe']
        # Add other fields as needed
    )