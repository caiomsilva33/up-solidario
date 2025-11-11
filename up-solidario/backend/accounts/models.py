from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de utilizador personalizado.
    Estende o User padrão do Django para adicionar o campo 'type'.
    """
    # Define as opções para o campo 'type' de forma organizada.
    class Types(models.TextChoices):
        DOADOR = "DOADOR", "Doador"
        ONG = "ONG", "ONG"
        ADMIN = "ADMIN", "Admin"

    # O campo 'type' para diferenciar os tipos de utilizador.
    # O default=Types.DOADOR significa que novos utilizadores serão doadores por padrão.
    type = models.CharField(
        max_length=50,
        choices=Types.choices,
        default=Types.DOADOR
    )