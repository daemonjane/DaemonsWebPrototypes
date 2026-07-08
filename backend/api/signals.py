from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver

from services.osimart import OsimartClient, OsimartError

User = get_user_model()


@receiver(post_delete, sender=User)
def delete_osimart_customer_on_user_delete(sender, instance, **kwargs):
    if instance.is_staff:
        return
    email = (instance.email or "").strip().lower()
    if not email:
        return
    try:
        client = OsimartClient()
        existing = client.get_customers(params={"search": email, "limit": 5})
        results = existing.get("results") if isinstance(existing, dict) else existing
        for c in (results or []):
            if c.get("email", "").strip().lower() == email:
                client.delete_customer(c["id"])
                break
    except OsimartError:
        pass
