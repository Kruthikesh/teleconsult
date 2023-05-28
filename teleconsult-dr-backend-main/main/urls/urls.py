'''
WSGI config for main(WoofyaAPIDashboard) project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
'''

import os

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.wsgi import get_wsgi_application
from django.urls import path, include
from main.settings.settings import MEDIA_URL, MEDIA_ROOT
from rest_framework import routers
from apps.patient.views import AuthViewSet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings.settings')

application = get_wsgi_application()

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls.api_urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
