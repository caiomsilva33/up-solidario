# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Importações das nossas views
from accounts.views import UserViewSet
from ongs.views import NGOViewSet
from campaigns.views import CampaignViewSet, DonationViewSet, StripeWebhookView
from .views import index

# Importações para os tokens JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Importações para a documentação
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Corrigido: removemos o argumento que causava o erro.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'ongs', NGOViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'donations', DonationViewSet)

urlpatterns = [
    path('painel-secreto/', admin.site.urls),
    path('', index, name='index'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]