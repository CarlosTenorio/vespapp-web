from django.conf.urls import url
from web.views import HomePageView
from web.views import NewSightingView
from web.views import SightingsView
from web.views import SightingView
from web.views import SightQuestionView
from web.views import UserSignupView
from web.views import UserLoginView
from web.views import UserLogoutView
from web.views import UserProfileView
from web.views import InfoView
from web.views import ContactView
from web.views import AboutView
from web.views import TeamView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^new_sighting/$', NewSightingView.new_sighting, name='new_sighting'),
    url(r'^sightings/$', SightingsView.as_view(), name='sightings'),
    url(r'^sighting/(?P<sighting_id>[0-9]+)/$', SightingView.sighting_view, name="sighting_id"),
    url(r'^sight_question/$', SightQuestionView.sight_question, name='sight_question'),

    url(r'^signup/$', UserSignupView.signup_user_view, name='signup'),
    url(r'^login/$', UserLoginView.login_view, name='login'),
    url(r'^logout/$', UserLogoutView.logout_view, name='logout'),
    url(r'^user_profile/$', UserProfileView.edit_profile, name='user_profile'),

    url(r'^info/$', InfoView.as_view(), name='info'),
    url(r'^contact/$', ContactView.contact_view, name='contact'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^team/$', TeamView.as_view(), name='team'),
]