from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView
from dashboard.views import DashboardView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "CityGame - Mission Control"
admin.site.index_title = "CityGame - Mission Control"
admin.site.site_title = "CityGame - Mission Control"

urlpatterns = [
    path("api/users/", include("users.urls")),
    path("api/", include("core.urls")),
    path("dashboard/", DashboardView.as_view()),
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
