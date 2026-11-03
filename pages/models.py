from wagtail.models import Page
from modelcluster.fields import ParentalKey
# ici, les champs du formulaire appartiennent a une page Contact precise
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet 
# register snippet: transforme le modèle Django classique en snippet Wagtail
from django import forms
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField

class CoachPage(Page):
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    def get_context(self, request):
        context = super().get_context(request)
        context["coachs_list"] = Coach.objects.all()
        return context


    content_panels = Page.content_panels + [
        FieldPanel("photo")
    ]

@register_snippet # je déclare mon DECORATEUR snippet
class Coach(models.Model):
    prenom = models.CharField("Prénom", max_length=100)
    presentation = models.TextField("presentation", blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        )
    cours = models.ManyToManyField("Cours", blank=True)
    jours_presence = models.CharField(
        "Jour de présence", max_length=200, blank=True, help_text="Ex : Lundi, Mercredi, vendredi",
        )

    panels = [
        FieldPanel("prenom"),
        FieldPanel("presentation"),
        FieldPanel("photo"),
        FieldPanel("cours", widget=forms.CheckboxSelectMultiple),
        FieldPanel("jours_presence"),
    ]

    def __str__(self):
        return self.prenom


@register_snippet
class Cours(models.Model):
   nom = models.CharField(max_length=100)
   horaires = models.CharField(max_length=100, blank=True)
   niveau = models.CharField(max_length=100, blank=True)
   description = models.TextField(blank=True)
   panels = [
       FieldPanel("nom"),
       FieldPanel("horaires"),
       FieldPanel("niveau"),
       FieldPanel("description")
   ]

   def __str__(self):
       return self.nom
       
class CoursPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context["cours_list"] = Cours.objects.all()
        return context   
    

class FormField(AbstractFormField): 
 # AbstractFormField fournit deja tout ce qu'il faut pour decrire UN champ
    # quelconque (label, type de champ, obligatoire ou non...). On ajoute juste
    # le lien vers la page Contact. Les vrais champs (Nom, Email, Message) ne sont
    # PAS ecrits ici : ils seront crees comme des donnees, depuis l'admin (etape 5).
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE, # si la page cotact est supprimée, ses champss le sont aussi
        related_name="form_fields",
    )

class ContactPage(AbstractEmailForm):
     # On remplace Page par AbstractEmailForm : ContactPage reste une page (AbstractEmailForm
    # herite de Page), mais une page qui sait aussi envoyer un email a chaque reponse.
    intro = RichTextField(blank=True) # texte affiche au-dessus du formulaire
    thank_you_text = RichTextField(blank=True) # message affiché après l'envoi
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        # InlinePanel : widget d'admin qui affiche la liste des FormField de cette page,
        # avec un bouton pour en ajouter, en retirer, ou changer leur ordre
        FieldPanel("thank_you_text"),
        FieldPanel("to_address"),    # l'email de Max, qui recevra chaque message
        FieldPanel("from_address"),  # l'adresse "expediteur" affichee sur l'email recu
        FieldPanel("subject"),       # le sujet de l'email envoye
    ]

class CoachsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro")
    ]

    # sous cette page ne poura être ajouter que des fiches de coach
    subpage_types = ["pages.CoachProfilPage"]

    # va les chercher dans la page coach profil page (pas encore créé) pour les afficher

    def get_context(self, request):
        context = super().get_context(request)
        context["coachs"] = CoachProfilPage.objects.child_of(self).live()

        return context 

class CoachProfilPage(Page):
    nom = models.CharField(max_length=100, blank=True)
    specialite = models.CharField(max_length=50)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    bio = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("nom"),
        FieldPanel("specialite"),
        FieldPanel("photo"),
        FieldPanel("bio")
    ]

    parent_page_types = ["pages.CoachsIndexPage"]