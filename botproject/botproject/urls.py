from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('bot/<int:botid>/message/', include('message.urls',
                                             namespace='message')),
    path('bot/<int:botid>/kr/', include('kr.urls', namespace='kr')),
    # path('bot/<int:botid>/quizzes/', include('quizzes.urls', namespace='quizzes')),
    path('bot/<int:botid>/group/', include('groups.urls', namespace='groups')),
    path('bot/<int:botid>/plan/', include('plans.urls', namespace='plans')),
    path('webhook/reg/', include('regbot.urls', namespace='regbot')),
    path('webhook/', include('edubot.urls', namespace='edubot')),
    path('bot/<int:botid>/works/', include('works.urls', namespace='works')),
    path('admin/', admin.site.urls),
    path('', include('login.urls', namespace='login')),
    path('', include('bots.urls', namespace='bots')),
]

handler404 = "botproject.views.page_not_found_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
