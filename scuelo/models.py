from django.db import models

CONDITION_ELEVE = (
    ("CONF", "CONF"),
    ("ABAN", "ABAN"),
    ("PROP", "PROP"),
)

HAND = (
    ("DA", "DA"),
    ("DM", "DM"),
    ("DL", "DL"),
    ("DV", "DV"),

)
CS_PY = (
    ("CS", "CS"),
    ("Extra", "EXTRA"),
    ("PY", "PY"),
)

SEX = (
    ("F", "F"),
    ("M", "M"),
)

CAUSAL = (
    ("insc", "inscription"),
    ("sco", "scolarite"),
    ("ten", "tenue"),
    ("can", "cantine"),
)
TYPE_ECOLE = (
    ("MATERNELLE", "MATERNELLE"),
    ("PRIMAIRE", "PRIMAIRE"),
)


class Classe(models.Model):
    type_ecole = models.CharField(max_length=14, choices=TYPE_ECOLE)
    nom = models.CharField(max_length=10, null=False)


class Eleve(models.Model):
    nom = models.CharField(max_length=34, null=False)
    prenom = models.CharField(max_length=34, null=False)
    date_enquete = models.DateTimeField(blank=True)  # is  added right after
    condition_eleve = models.CharField(
        max_length=4,
        choices=CONDITION_ELEVE
    )
    sex = models.CharField(max_length=1, choices=SEX)
    date_naissance = models.DateField()
    cs_py = models.CharField(max_length=6, choices=CS_PY)
    hand = models.CharField(max_length=2, choices=HAND, default="")
    annee_inscr = models.CharField(max_length=4)  # the inscrption year
    parent = models.CharField(max_length=34, null=False)
    tel_parent = models.CharField(max_length=24, null=False)
    note_eleve = models.CharField(max_length=240, blank=True, default='')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    @property
    def an_insc(self):
        return self.annee_inscr.year

    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        messages.success(request, f'vous avez enregister l\'eleve {self.nom} {self.prenom} de la classe  de  {self.nom_classe}') 
    '''

    def get_queryset(self, request):
        # Group students by nom_classe
        queryset = Eleve.objects.all().prefetch_related('nom_classe')  # Prefetch for efficiency
        grouped_queryset = {}
        for eleve in queryset:
            classe = eleve.nom_classe.pk  # Get the primary key of nom_classe
            if classe not in grouped_queryset:
                grouped_queryset[classe] = []
            grouped_queryset[classe].append(eleve)
        return grouped_queryset

    class Meta:
        verbose_name = 'Eleve'
        # order_by = 'nom_classe'

        verbose_name_plural = 'Eleves'


class AnneeScolaire(models.Model):
    nom = models.CharField(max_length=100)
    date_initiale = models.DateField(blank=True)
    date_finale = models.DateField(blank=True)
    actuel = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.actuel:
            AnneeScolaire.objects.filter(actuel=True).exclude(pk=self.pk).update(actuel=False)


class Inscription(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)