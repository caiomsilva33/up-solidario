from django.db import models
from django.conf import settings

class NGO(models.Model):
    class StatusChoices(models.TextChoices):
        EM_ANALISE = "EM_ANALISE", "Em Análise"
        VERIFICADO = "VERIFICADO", "Verificado"
        RECUSADO = "RECUSADO", "Recusado"

    # Ligação um-para-um com o nosso modelo de utilizador.
    # Cada ONG está associada a um único utilizador.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    status_verificacao = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.EM_ANALISE
    )
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome