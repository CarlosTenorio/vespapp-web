from django.conf.urls import url
from api import views as api_views

urlpatterns = [
    url(r'^sightings/$', api_views.SightingListCreateView.as_view(), name='sightings_list_create'),

    url(r'^sightings/(?P<sighting_id>[0-9]+)/$',
        api_views.SightingRetrieveUpdateView.as_view(), name='sightings_retrieve_update'),
    
    url(r'^sightings/(?P<sighting_id>[0-9]+)/photos/$',
        api_views.SightingPictureCreateView.as_view()),

    url(r'^sightings/(?P<sighting_id>[0-9]+)/questions/$', api_views.SightingQuestionsListView.as_view(),
        name='sightings_questions'),

    url(r'locations/', api_views.LocationsList.as_view(), name='location_list'),

    url(r'provinces/', api_views.ProvincesList.as_view(), name='province_list'),

    url(r'info/', api_views.SightingInfoList.as_view(), name='info_list')







    #url(r'^sightings/(?P<sighting_id>[0-9]+)/user_comments/$', api_views.SightingUserCommentsListView.as_view(), name='sightings_user_comments'),

    #url(r'^sightings/(?P<sighting_id>[0-9]+)/expert_comments/$', api_views.SightingExpertCommentsListView.as_view(), name='sightings_expert_comments')
]