from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from server.views import ServerListViewSet

# Initialize the default router for API routes
router = DefaultRouter()
router.register("api/server/select", ServerListViewSet)

# Define URL patterns
urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    # API schema endpoint for generating OpenAPI documentation
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API documentation UI using Swagger
    path("api/docs/schema/ui/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
] + router.urls

# Add media file serving in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
