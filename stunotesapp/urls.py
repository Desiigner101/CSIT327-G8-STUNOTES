from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Use the notes app's root landing page as the project's default root.
    # The logic for redirecting to login vs. landing (first-run) is handled in `notes.views.landing_view`.
    path('', include('notes.urls')),
    #path('test/', include('stunotes.urls')),
    
    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)