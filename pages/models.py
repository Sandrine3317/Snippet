from wagtail.models import Page
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet 
from django import forms

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

@register_snippet
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
    

class ContactPage(Page):
    pass
