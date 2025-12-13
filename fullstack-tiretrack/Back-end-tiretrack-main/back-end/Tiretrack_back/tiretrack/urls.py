from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.serializers import CustomTokenObtainPairSerializer

# View de Login customizada (definida aqui ou importada de core.views se preferir)
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

schema_view = get_schema_view(
    openapi.Info(
        title="TireTrack API",
        default_version="v1",
        description="API de gestão de pneus",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Rotas de Autenticação
    path("api/token/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Rota Principal da API (Aponta para o arquivo core/urls.py)
    path("api/", include("core.urls")),
    
    # Documentação
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]