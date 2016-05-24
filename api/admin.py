from django.contrib import admin

from api.models import *

class SightingAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'location','created_at')
    fieldsets = [('Información básica', {'fields': ['id',('created_at', 'source')]}), 
    ('Datos del usuario', {'fields': [('user', 'contact')]}), 
    ('Localización del avispamiento', {'fields': [('location', 'lat', 'lng')]}),
    ('Datos del avispamiento', {'fields': [('type','glosario_tipos'), 'free_text', 'foto_avispamiento', ('respuestas_preguntas')]}),
    ('Estado del avispamiento', {'fields': [('public'), ('status', 'glosario_estados'), ('is_valid', 'moderator')]}),
    ('Comentarios de expertos', {'fields': ['comentarios_expertos']}),
    ('Comentarios de usuarios', {'fields': ['comentarios_usuarios']}),]
    readonly_fields = ['id','created_at', 'foto_avispamiento', 'glosario_tipos', 'glosario_estados','respuestas_preguntas', 'comentarios_expertos','comentarios_usuarios',]
    list_filter = ('created_at','status','type', 'public', 'is_valid', 'source', 'location', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    fieldsets = [('Pregunta', {'fields': ['title', ('question_type', 'glosario_preguntas'), ('sighting_type', 'glosario_tipo_pregunta'), 'order','is_active']}),]
    readonly_fields = ['glosario_preguntas','glosario_tipo_pregunta',]
    list_filter = ('question_type',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'value', 'created_at')
    fieldsets = [('Respuesta', {'fields': ['created_at', 'question', 'value']}),]
    readonly_fields = ['created_at',]
    list_filter = ('question',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fieldsets = [('Perfil del usuario', {'fields': ['user', ('foto_usuario', 'photo')]}),]
    readonly_fields = ['foto_usuario',]


class SightingInfoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = [('INFO', {'fields': ['title', 'quickBody', 'body', ('foto_portada', 'imageCover'), ('foto_info', 'image')]}),]
    readonly_fields = ['foto_portada', 'foto_info']


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'sighting', 'created_at')
    fieldsets = [('Foto', {'fields': ['id', 'sighting', 'created_at', ('foto', 'file')]}),]
    readonly_fields = ['id', 'foto', 'created_at']


class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'sighting')
    list_filter = ('sighting', 'user',)


class ExpertCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'sighting', 'is_valid')
    list_filter = ('sighting', 'user', 'is_valid')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Sighting, SightingAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(UserComment, UserCommentAdmin)
admin.site.register(ExpertComment, ExpertCommentAdmin)
admin.site.register(SightingInfo, SightingInfoAdmin)
admin.site.register(Location)
admin.site.register(Province)
admin.site.register(UserProfile, UserProfileAdmin)

#class AnswerAdmin (admin.ModelAdmin):
 #   model=Sighting
  #  filter_horizontal = ('answers',)
    # exclude = ('source',)