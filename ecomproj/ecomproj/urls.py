from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storeapp.urls')),
    path('cartapp/', include('cartapp.urls')),
    # below connects the main url (ecomproj) to the new app (paymentapp)
    path('paymentapp/', include('paymentapp.urls')),
    # Below uploads pictures and videos
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
