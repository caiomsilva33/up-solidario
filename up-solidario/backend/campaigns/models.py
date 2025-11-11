from django.db import models
from django.conf import settings
from ongs.models import NGO

class Campaign(models.Model):
    class StatusChoices(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        PAUSADA = "PAUSADA", "Pausada"
        CONCLUIDA = "CONCLUIDA", "Concluída"
        CANCELADA = "CANCELADA", "Cancelada"

    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name='campaigns')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    meta = models.DecimalField(max_digits=10, decimal_places=2)
    arrecadado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    urgencia = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.ATIVA)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Donation(models.Model):
    class StatusChoices(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        CONFIRMADA = "CONFIRMADA", "Confirmada"
        FALHOU = "FALHOU", "Falhou"

    class MethodChoices(models.TextChoices):
        PIX = "PIX", "Pix"
        CARTAO = "CARTAO", "Cartão de Crédito"
        BOLETO = "BOLETO", "Boleto"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='donations')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50, choices=MethodChoices.choices)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDENTE)
    tx_id = models.CharField(max_length=255, blank=True, null=True)
    data_doacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Doação de {self.valor} para {self.campaign.titulo}'