# api/campaigns/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction # <-- Importação para transações
import stripe
from rest_framework.permissions import AllowAny

from .models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer
from core.permissions import IsOngUser

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsOngUser]

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    @action(detail=True, methods=['post'])
    def create_checkout_session(self, request, pk=None):
        donation = self.get_object()
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'brl',
                            'product_data': {
                                'name': f"Doação para: {donation.campaign.titulo}",
                            },
                            'unit_amount': int(donation.valor * 100),
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'donation_id': donation.id
                },
                mode='payment',
                success_url='http://localhost:8001?success=true',
                cancel_url='http://localhost:8001?canceled=true',
            )
            return Response({'url': checkout_session.url})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            donation_id = session.get('metadata', {}).get('donation_id')
            
            if donation_id:
                try:
                    # --- OTIMIZAÇÃO DE CONSISTÊNCIA DE DADOS: TRANSAÇÃO ---
                    # Este bloco garante que todas as operações dentro dele
                    # (salvar a doação e criar o evento de pontos no sinal)
                    # aconteçam com sucesso, ou nenhuma acontece.
                    with transaction.atomic():
                        donation = Donation.objects.get(id=donation_id)
                        donation.status = Donation.StatusChoices.CONFIRMADA
                        donation.save()
                except Donation.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)