# api/accounts/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated # <-- 1. IMPORTE IsAuthenticated
from .models import User
from .serializers import UserSerializer
from core.permissions import IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API que permite que os utilizadores sejam vistos ou editados.
    - Administradores veem todos os utilizadores.
    - Utilizadores normais veem apenas a si mesmos.
    """
    serializer_class = UserSerializer
    
    # --- A CORREÇÃO ESTÁ AQUI ---
    # Aplicamos AMBAS as permissões. O DRF irá verificá-las por ordem.
    # Primeiro, verifica se o utilizador está autenticado.
    # Depois (para endpoints de detalhe), verifica se é o dono ou admin.
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Este método personaliza a lista de resultados.
        """
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)