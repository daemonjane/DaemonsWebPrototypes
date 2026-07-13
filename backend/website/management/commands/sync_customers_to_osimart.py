"""Sync existing local users to Osimart as customers."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from services.osimart import OsimartClient, OsimartError
from website.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Push all local non-staff users to Osimart as customers."

    def handle(self, *args, **options):
        users = User.objects.filter(is_staff=False).order_by("date_joined")
        total = users.count()
        if total == 0:
            self.stdout.write("No local users to sync.")
            return

        self.stdout.write(f"Found {total} local user(s) to sync...")

        try:
            client = OsimartClient()
        except Exception as e:
            self.stderr.write(f"Failed to initialize OsimartClient: {e}")
            return

        created = 0
        skipped = 0
        errors = []

        for user in users:
            first_name = user.first_name or user.username.split()[0] if user.username else ""
            last_name = user.last_name or ""
            email = user.email
            if not email:
                self.stdout.write(f"  SKIP user #{user.id}: no email")
                skipped += 1
                continue

            try:
                existing = client.get_customers(params={"search": email, "limit": 10})
                results = existing.get("results") if isinstance(existing, dict) else existing
                already_exists = any(
                    r.get("email", "").strip().lower() == email.strip().lower()
                    for r in (results or [])
                )
                if already_exists:
                    self.stdout.write(f"  SKIP {email}: already exists in Osimart")
                    skipped += 1
                    continue
            except OsimartError:
                pass

            safe_last = last_name or first_name.split()[-1] if first_name.split() else "_"
            safe_first = first_name or email.split("@")[0]

            try:
                resp = client.create_customer({
                    "email": email,
                    "first_name": safe_first,
                    "last_name": safe_last,
                    "is_guest": True,
                    "mobile_number": "0000000000",
                })

                if user.email:
                    profile, _ = UserProfile.objects.get_or_create(user=user)
                    customer_id = resp.get("id") if isinstance(resp, dict) else None
                    if customer_id:
                        profile.osimart_customer_id = str(customer_id)
                        profile.save(update_fields=["osimart_customer_id"])
                self.stdout.write(f"  OK   {email}")
                created += 1
            except OsimartError as e:
                if e.response_body and "already" in str(e.response_body).lower():
                    self.stdout.write(f"  SKIP {email}: already exists (server says)")
                    skipped += 1
                else:
                    detail = e.response_body or str(e)
                    self.stderr.write(f"  ERROR {email}: {detail}")
                    errors.append(email)
            except Exception as e:
                self.stderr.write(f"  ERROR {email}: {e}")
                errors.append(email)

        self.stdout.write(f"\nDone. Created: {created}, Skipped: {skipped}, Errors: {len(errors)}")
        if errors:
            self.stderr.write(f"Errors: {', '.join(errors)}")
