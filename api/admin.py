from django.contrib import admin

from api.models import *

class AnswerAdmin (admin.ModelAdmin):
	model=Sighting
	filter_horizontal = ('answers',)
	# exclude = ('source',)


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Sighting, AnswerAdmin)
admin.site.register(Picture)
admin.site.register(UserComment)
admin.site.register(ExpertComment)
admin.site.register(SightingFAQ)
admin.site.register(Location)
admin.site.register(Province)
admin.site.register(UserProfile)

