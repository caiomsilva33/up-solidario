# api/campaigns/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation
from gamification.models import PointEvent
import math

@receiver(post_save, sender=Donation)
def award_points_on_donation_confirmation(sender, instance, created, **kwargs):
    if instance.status == Donation.StatusChoices.CONFIRMADA and instance.user:
        # --- A CORREÇÃO ESTÁ AQUI ---
        # Incluímos o ID da doação para tornar a razão única para cada pagamento.
        reason_text = f"Doação #{instance.id} para a campanha '{instance.campaign.titulo}'"
        
        if not PointEvent.objects.filter(user=instance.user, reason=reason_text).exists():
            points_to_award = math.floor(float(instance.valor))
            if points_to_award > 0:
                PointEvent.objects.create(
                    user=instance.user,
                    points=points_to_award,
                    reason=reason_text
                )