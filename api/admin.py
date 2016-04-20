from django.contrib import admin

from api.models import *


class SightingAdmin(admin.ModelAdmin):

    list_display = ('id','user', 'location','created_at')

    fieldsets = [('Información básica', {'fields': ['id',('created_at', 'source')]}), 
    ('Datos del usuario', {'fields': [('user', 'contact')]}), 
    ('Localización del avispamiento', {'fields': [('location', 'lat', 'lng')]}),
    ('Datos del avispamiento', {'fields': [('type','glosario_tipos'), 'free_text', 'foto_avispamiento', ('answers', 'respuestas_preguntas')]}),
    ('Estado del avispamiento', {'fields': [('public'), ('status', 'glosario_estados'), ('is_valid', 'moderator')]}),]
    readonly_fields = ['id','created_at', 'foto_avispamiento', 'glosario_tipos', 'glosario_estados','respuestas_preguntas',]
    list_filter = ('created_at','status','type', 'public', 'is_valid', 'source', 'location',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    fieldsets = [('Pregunta', {'fields': ['title', ('question_type', 'glosario_preguntas'), ('sighting_type', 'glosario_tipo_pregunta'), 'is_active']}),]
    readonly_fields = ['glosario_preguntas','glosario_tipo_pregunta',]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    fieldsets = [('Perfil del usuario', {'fields': ['user', ('foto_usuario', 'photo')]}),]
    readonly_fields = ['foto_usuario',]


class SightingFAQAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fieldsets = [('FAQ', {'fields': ['title', 'quickBody', 'body', ('foto_faq', 'image')]}),]
    readonly_fields = ['foto_faq',]


class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'sighting', 'created_at')
    fieldsets = [('Foto', {'fields': ['id', 'sighting', 'created_at', ('foto', 'file')]}),]
    readonly_fields = ['id', 'foto', 'created_at']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Sighting, SightingAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(UserComment)
admin.site.register(ExpertComment)
admin.site.register(SightingFAQ, SightingFAQAdmin)
admin.site.register(Location)
admin.site.register(Province)
admin.site.register(UserProfile, UserProfileAdmin)

