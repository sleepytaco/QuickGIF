from django.conf.urls import include, url
from quick_gif.views import quick_gif, view_quick_gif, generate_gif_link
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
    url(r"QuickGIF", quick_gif, name="quick_gif"),
    url(r'^generate-gif-link/$', generate_gif_link, name='generate_gif_link'),
    url("^permalink/(?P<key>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$",
        view_quick_gif),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
