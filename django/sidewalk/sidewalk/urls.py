from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sidewalk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) 

urlpatterns += patterns('authenticate.views',

    url(r'^$', 'index'),
    url(r'^home/$', 'home'),
    url(r'^login/$', 'login_view'),
    url(r'^comments/$', 'comments'),
    url(r'^register/$', 'register'),
    url(r'^dash/$', 'dash'),
    url(r'^dash/current/$', 'dash_next_current_page'),
    url(r'^dash/trending/$', 'dash_next_trending_page'),
    url(r'^dash/complete$', 'completion'),
    url(r'^dash/forfeit$', 'forfeit'),
    url(r'^dash/accept$', 'accept'),
    url(r'^dash/allied/$', 'dash_next_allied_page'),
    url(r'^dash/completion-form$', 'complete_challenges_form'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$', 'profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/ally$', 'make_ally'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/de-ally$', 'remove_ally'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/timeline/$', 'timeline'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/timeline/quest/$', 'timeline_quest'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/timeline/comment$', 'comment'),
    url(r'^account/$', 'settings'),
    url(r'^account/submit/$', 'settings_submit'),
    url(r'^account/errors/$', 'settings_errors'),
    url(r'^logout/$', 'logout_view'),
    url(r'^help/$', 'help')
    # EXTRA: Add code and corresponding URL for initial usage
)

urlpatterns += patterns('qsearch.views',

    url(r'^search/$', 'index'),
    url(r'^search/keywords/(?P<model>[a-z]+)/$', 'keywords'),
    url(r'^search/submit/$', 'submit'),
    url(r'^search/errors/$', 'search_errors'),
    url(r'^search/(?P<keyword>[a-zA-Z0-9]+)/$', 'query') 

    # TODO: Possible filter encoding in HTTP if browser can't handle memory.
    # Or handle client-side. 

#     # EXTRA: Add code and corresponding URL for initial usage
)

#urlpatterns += patterns('qview.views',
#    url(r'^view/$', 'index'),
#    url(r'^view/current/$', 'current'),
#    url(r'^view/current/keywords/$', 'current_keywords'),
#    url(r'^view/completed/$', 'completed'),
#    url(r'^view/completed/keywords/$', 'completed_keywords'),
#     # EXTRA: Add code and corresponding URL for initial usage
#)

urlpatterns += patterns('qpost.views',
    url(r'^post/$', 'post'),
    url(r'^post/submit$', 'submission'),
    url(r'^post/success/$', 'post_success'),
    url(r'^quest/(?P<quest_id>[1-9][0-9]*)-(?P<quest_poster>[a-zA-Z0-9]+)/$', 'quest'),
    url(r'^quest/(?P<quest_id>[1-9][0-9]*)-(?P<quest_poster>[a-zA-Z0-9]+)/complete$', 'completion'),
    url(r'^quest/(?P<quest_id>[1-9][0-9]*)-(?P<quest_poster>[a-zA-Z0-9]+)/accept$', 'accept'),
    url(r'^quest/(?P<quest_id>[1-9][0-9]*)-(?P<quest_poster>[a-zA-Z0-9]+)/remove$', 'remove'),
    url(r'^quest/(?P<quest_id>[1-9][0-9]*)-(?P<quest_poster>[a-zA-Z0-9]+)/forfeit$', 'forfeit')
    # TODO: Encode form response into HTTP! If necessary.
    # EXTRA: Add code and corresponding URL for initial usage
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
