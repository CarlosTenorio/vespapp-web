from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Province(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nombre')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nombre')

    lat = models.FloatField(null=False, blank=False, verbose_name='Latitud')
    lng = models.FloatField(null=False, blank=False, verbose_name='Longitud')

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, related_name="provinces",
                                 verbose_name='Provincia', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Localización'
        verbose_name_plural = 'Localizaciones'

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPE_RADIO = 1
    TYPE_CHECKBOX = 2

    title = models.CharField(max_length=128, null=False, blank=False, verbose_name='Título')
    question_type = models.IntegerField(verbose_name="Tipo de pregunta")
    sighting_type = models.IntegerField(null=False, blank=False, verbose_name="Tipo de avistamiento")
    is_active = models.BooleanField(default=True, null=False, blank=False, verbose_name="Activa")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def glosario_preguntas(self):
            return '1: Solo una respuesta - 2: Múltiples respuestas'

    glosario_preguntas.allow_tags = True

    def glosario_tipo_pregunta(self):
            return '1: Avispa - 2: Nido'

    glosario_tipo_pregunta.allow_tags = True

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="default_answer")

    value = models.CharField(max_length=128, null=False, blank=False, verbose_name='Título')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return self.value


class Sighting(models.Model):
    STATUS_PENDING = 0
    STATUS_PROCESSING = 1
    STATUS_PROCESSED = 2

    TYPE_WASP = 1
    TYPE_NEST = 2

    lat = models.FloatField(null=True, blank=True, verbose_name='Latitud')
    lng = models.FloatField(null=True, blank=True, verbose_name='Longitud')

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name="sightings",
                                 verbose_name='Localización', null=True, blank=True)

    status = models.IntegerField(null=False, blank=False, verbose_name="Estado", default=STATUS_PENDING)
    free_text = models.CharField(null=True, blank=True, max_length=512, verbose_name='Texto sobre localización')

    contact = models.CharField(null=True, blank=True, max_length=128, verbose_name='Contacto')
    user = models.ForeignKey(User, related_name="user_sighthing", verbose_name='Avispamiento de', null=True,
                                    blank=True)

    type = models.IntegerField(null=False, blank=False, verbose_name="Tipo de avistamiento")
    public = models.BooleanField(null=False, blank=False, default=False, verbose_name='Publico')

    reported_by = models.ForeignKey(User, related_name="reported_sightings", verbose_name='Reportado por', null=True,
                                    blank=True)
    moderator = models.ForeignKey(User, related_name="moderated_sightings", verbose_name='Moderador', null=True,
                                  blank=True)
    is_valid = models.NullBooleanField(verbose_name="Avistamiento válido", null=True, default=None)

    answers = models.ManyToManyField(Answer, related_name="sightings", default=None, blank=True, verbose_name='Respuestas')

    source = models.CharField(max_length=128, verbose_name='Fuente')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    @property
    def first_picture(self):
        if self.pictures.count():
            return self.pictures.first()
        else:
            return None
    
    def foto_avispamiento(self):
        pictures= self.pictures.all()
        images=''
        for x in pictures:
            images= images + '<a href="%s"><img hspace="5px" src="%s" width=200px heigth=200px/></a>'%(x.file.url, x.file.url)
        return images

    foto_avispamiento.allow_tags = True

    def glosario_tipos(self):
            return '1: Avispa - 2: Nido'

    glosario_tipos.allow_tags = True

    def glosario_estados(self):
            return '0: Pendiente 1: Procesando 2: Procesado'

    glosario_estados.allow_tags = True

    def respuestas_preguntas(self):
        answers= self.answers.all()
        ans=''
        if self.answers.count():
            for j in answers:
                ans= ans + '</br>' + '<p><b>%s</b></p>'%(j.question) + '</br>' + j.value
            return ans
        else:
            return 'No hay respuestas'

    respuestas_preguntas.allow_tags = True

    class Meta:
        verbose_name = 'Avispamiento'
        verbose_name_plural = 'Avispamientos'

    def __str__(self):
        return "{}".format(self.id)


class Picture(models.Model):
    file = models.ImageField(null=False, blank=False, upload_to="sightings/")
    sighting = models.ForeignKey(Sighting, null=False, blank=False, related_name='pictures')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def foto(self):
        return '<a href="%s"><img src="%s" width=250px heigth=250px/></a>'%(self.file.url, self.file.url)

    foto.allow_tags = True

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'


class ExpertComment(models.Model):
    user = models.ForeignKey(User, related_name="expert_comments", null=True)
    sighting = models.ForeignKey(Sighting, related_name="expert_comments")

    body = models.CharField(null=False, blank=False, max_length=512, verbose_name='Comentario')

    is_valid = models.NullBooleanField(verbose_name="Avistamiento válido")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Comentario de experto'
        verbose_name_plural = 'Comentarios de experto'

    def __str__(self):
        return self.body


class UserComment(models.Model):
    user = models.ForeignKey(User, related_name="user_comments")
    sighting = models.ForeignKey(Sighting, related_name="user_comments")
    body = models.CharField(null=False, blank=False, max_length=512, verbose_name='Comentario')

    moderated = models.BooleanField(verbose_name="Moderado", default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    class Meta:
        verbose_name = 'Comentario de usuario'
        verbose_name_plural = 'Comentarios de usuario'

    def __str__(self):
        return self.body


class SightingFAQ(models.Model):
    title = models.CharField(null=False, blank=False, max_length=128, verbose_name='Título')
    body = models.TextField(verbose_name='Explicación más detallada')
    quickBody = models.TextField(null=False, blank=False, default="Clic para más información", max_length=128, verbose_name='Breve explicación')
    image = models.ImageField(upload_to="faq_images/", blank=True, null=True)
    
    def foto_faq(self):
        return '<a href="%s"><img src="%s" width=250px heigth=250px/></a>'%(self.image.url, self.image.url)

    foto_faq.allow_tags = True

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.title





#REGISTRATION
class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)
    
    def foto_usuario(self):
        return '<a href="%s"><img src="%s" width=250px heigth=250px/></a>'%(self.photo.url, self.photo.url)

    foto_usuario.allow_tags = True

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'

    def __str__(self):
        return self.user.username