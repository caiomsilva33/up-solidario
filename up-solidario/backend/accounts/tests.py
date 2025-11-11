# api/accounts/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User

class UserAPITests(APITestCase):
    """
    Suite de testes para o endpoint de Utilizadores.
    """

    def setUp(self):
        """
        Este método é executado antes de cada teste.
        Usamo-lo para criar os dados de que os nossos testes irão precisar.
        """
        # Criamos um utilizador normal (Doador)
        self.normal_user = User.objects.create_user(
            username='doador_teste', 
            password='senha_segura_123',
            email='doador@teste.com',
            type='DOADOR'
        )

        # Criamos um utilizador administrador
        self.admin_user = User.objects.create_superuser(
            username='admin_teste', 
            password='senha_segura_123',
            email='admin@teste.com'
        )
        # Por defeito, o superuser é 'staff', o que lhe dá permissões de admin.
        # O tipo do superuser será o default ('DOADOR'), mas o que importa é o 'is_staff'.

        # URL para a lista de utilizadores
        self.list_url = reverse('user-list')

    def test_unauthenticated_user_cannot_access_list(self):
        """
        Cenário 1: Garante que um utilizador não autenticado recebe um erro 401 (Não Autorizado).
        """
        # Fazemos um pedido GET para a lista de utilizadores sem fazer login
        response = self.client.get(self.list_url)
        
        # Verificamos se o código de status da resposta é 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_sees_only_self(self):
        """
        Cenário 2: Garante que um utilizador normal vê apenas o seu próprio perfil.
        """
        # Forçamos a autenticação como o nosso utilizador normal
        self.client.force_authenticate(user=self.normal_user)
        
        # Fazemos o pedido GET como este utilizador
        response = self.client.get(self.list_url)
        
        # Verificamos se a resposta foi bem-sucedida (200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificamos se a resposta contém apenas 1 resultado
        self.assertEqual(len(response.data), 1)
        
        # Verificamos se o resultado é de facto o nosso utilizador normal
        self.assertEqual(response.data[0]['username'], self.normal_user.username)

    def test_admin_user_sees_all_users(self):
        """
        Cenário 3: Garante que um utilizador admin vê todos os utilizadores.
        """
        # Forçamos a autenticação como o nosso utilizador admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Fazemos o pedido GET como este utilizador
        response = self.client.get(self.list_url)

        # Verificamos se a resposta foi bem-sucedida (200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificamos se a resposta contém os 2 utilizadores que criámos
        self.assertEqual(len(response.data), 2)