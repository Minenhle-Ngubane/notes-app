from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", include("landing.urls", namespace="landing")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("notes/", include("note.urls", namespace="note")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)