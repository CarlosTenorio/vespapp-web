from django.conf.urls import url
from web.views import HomePageView
from web.views import FAQView
from web.views import SightingExpertCommentsView
from web.views import SightingView
from web.views import SightingsView
from web.views import SightQuestionView
from web.views import LocationsPageView
from web.views import SightingCommentView
from web.views import SightingCommentsView
from web.views import SightExpertCommentView
from web.views import NewSightingView
from web.views import UserSignupView
from web.views import UserLoginView
from web.views import UserLogoutView
from web.views import UserProfileView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^faq/$', FAQView.as_view(), name='faq'),
    url(r'^locations/$', LocationsPageView.as_view(), name='locations'),
    url(r'^new_sighting/$', NewSightingView.new_sighting, name='new_sighting'),

    url(r'^sightings/$', SightingsView.as_view(), name='sightings'),
    url(r'^sighting/(?P<sighting_id>[0-9]+)/$', SightingView.sighting_view, name="sighting_id"),
    url(r'^sight_question/$', SightQuestionView.sight_question, name='sight_question'),

    url(r'^sighting/(?P<sighting_id>[0-9]+)/expert_comments/$', SightingExpertCommentsView.as_view(), name='sighting_expert_comments'),
    url(r'^sighting/(?P<sighting_id>[0-9]+)/expert_comments/(?P<expert_comment_id>[0-9]+)$', SightExpertCommentView.as_view(), name='sight_expert_comment'),

    url(r'^sighting/(?P<sighting_id>[0-9]+)/user_comments/$', SightingCommentsView.as_view(), name='sighting_comments'),
    url(r'^sighting/(?P<sighting_id>[0-9]+)/user_comment/(?P<comment_id>[0-9]+)/$', SightingCommentView.as_view(), name='sighting_comment'),

    url(r'^signup/$', UserSignupView.signup_user_view, name='signup'),
    url(r'^login/$', UserLoginView.login_view, name='login'),
    url(r'^logout/$', UserLogoutView.logout_view, name='logout'),

    url(r'^user_profile/$', UserProfileView.edit_profile, name='user_profile'),

]