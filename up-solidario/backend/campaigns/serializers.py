# api/campaigns/serializers.py
from rest_framework import serializers
from .models import Campaign, Donation
from accounts.serializers import UserSerializer # Importamos o UserSerializer

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class DonationSerializer(serializers.ModelSerializer):
    # --- OTIMIZAÇÃO PARA O FRONTEND: SERIALIZADORES ANINHADOS ---
    # Incluímos os detalhes do utilizador na resposta da doação.
    user = UserSerializer(read_only=True)
    # Incluímos o título da campanha na resposta para fácil exibição.
    campaign_title = serializers.CharField(source='campaign.titulo', read_only=True)

    class Meta:
        model = Donation
        # Adicionamos os novos campos à lista de campos a serem exibidos.
        # 'campaign' continua a ser o ID da campanha, útil para o frontend fazer outras ações.
        fields = ['id', 'user', 'campaign', 'campaign_title', 'valor', 'metodo', 'status', 'data_doacao']