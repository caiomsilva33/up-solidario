# api/core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOngUser(BasePermission):
    """
    Permissão personalizada que:
    - Permite pedidos de leitura (GET) a qualquer utilizador autenticado.
    - Permite pedidos de escrita (POST, PUT, etc.) apenas a utilizadores do tipo 'ONG'.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.type == 'ONG'

# --- NOSSA NOVA PERMISSÃO ---
class IsOwnerOrAdmin(BasePermission):
    """
    Permissão personalizada para permitir que apenas os donos de um objeto ou administradores o editem/vejam.
    """
    def has_object_permission(self, request, view, obj):
        # Admins (is_staff) podem aceder a qualquer objeto.
        if request.user.is_staff:
            return True
        
        # O 'dono' do objeto pode aceder.
        # Assumimos que o objeto ('obj') é o próprio utilizador.
        return obj == request.user