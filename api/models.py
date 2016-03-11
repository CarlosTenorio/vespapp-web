from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nombre')

    lat = models.FloatField(null=False, blank=False, verbose_name='Latitud')
    lng = models.FloatField(null=False, blank=False, verbose_name='Longitud')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class Question(models.Model):
    TYPE_RADIO = 1
    TYPE_CHECKBOX = 2

    title = models.CharField(max_length=128, null=False, blank=False, verbose_name='Título')
    question_type = models.IntegerField(verbose_name="Tipo de pregunta")

    is_active = models.BooleanField(default=True, null=False, blank=False, verbose_name="Activa")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="default_answer")

    value = models.CharField(max_length=128, null=False, blank=False, verbose_name='Título')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class Sighting(models.Model):
    STATUS_PENDING = 0
    STATUS_PROCESSING = 1
    STATUS_PROCESSED = 2

    TYPE_WASP = 0
    TYPE_NEST = 1

    lat = models.FloatField(null=False, blank=False, verbose_name='Latitud')
    lng = models.FloatField(null=False, blank=False, verbose_name='Longitud')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="sightings",
                                 verbose_name='Localización')

    status = models.IntegerField(null=False, blank=False, verbose_name="Estado", default=STATUS_PENDING)
    free_text = models.CharField(null=False, blank=False, max_length=512, verbose_name='Texto sobre localización')

    type = models.IntegerField(null=False, blank=False, verbose_name="Tipo de avistamiento")
    public = models.BooleanField(null=False, blank=False, default=False, verbose_name='Publicado')

    reported_by = models.ForeignKey(User, related_name="Usuario reportador")
    moderator = models.ForeignKey(User, related_name="Experto moderador")

    answers = models.ManyToManyField(Answer, related_name="sightings")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class Picture(models.Model):
    file = models.ImageField(null=False, blank=False, upload_to="sightings/")
    sighting = models.ForeignKey(Sighting, null=False, blank=False, related_name='pictures')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class ExpertComment(models.Model):
    user = models.ForeignKey(User, related_name="expert_comments")
    body = models.CharField(null=False, blank=False, max_length=512, verbose_name='Comentario')

    is_valid = models.NullBooleanField(verbose_name="Avistamiento válido")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')


class UserComment(models.Model):
    user = models.ForeignKey(User, related_name="user_comments")
    body = models.CharField(null=False, blank=False, max_length=512, verbose_name='Comentario')

    moderated = models.BooleanField(verbose_name="Moderado")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
