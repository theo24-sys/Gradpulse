from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('auth/', include('accounts.auth_urls')),
    path('campus/', include('accounts.campus_urls')),
    path('corporate/', include('accounts.corporate_urls')),
    path('opportunities/', include('opportunities.urls')),
    path('grades/', include('grades.urls')),
    path('credentials/', include('credentials.urls')),
    path('events/', include('events.urls')),
    path('networking/', include('networking.urls')),
    path('notifications/', include('notifications.urls')),
    path('library/', include('library.urls')),
    # Support /scraping without trailing slash (some links omit it)
    path('scraping', include('scraping.urls')),
    path('scraping/', include('scraping.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
