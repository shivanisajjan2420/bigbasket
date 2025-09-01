from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", store_views.home, name="home"),       
    path("store/", include("store.urls")),     
    path("payments/", include("payments.urls")),     
    #path("support/", include("support.urls")),       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
