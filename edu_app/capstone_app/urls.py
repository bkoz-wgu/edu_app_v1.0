from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('',views.index,name="index"),
    path('app/', include('tests.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += static(settings.STATIC_URL,documents_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,documents_root=settings.MEDIA_ROOT)
