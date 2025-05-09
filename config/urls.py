from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenViewBase,
    TokenRefreshView,
    TokenVerifyView, TokenObtainPairView
)


class JWTSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        security_definitions = super().get_security_definitions()
        security_definitions['Bearer'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        return security_definitions


schem_view = get_schema_view(
    openapi.Info(
        title="API E-Commerce",
        default_version="v1",
        description="E-Commerce API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="komronbek@gmail.com"),
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=JWTSchemaGenerator
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('products.urls')),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schem_view.without_ui(cache_timeout=0), name='schem-json'),
    path('', schem_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schem_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
