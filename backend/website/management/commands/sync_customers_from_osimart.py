"""Pull all Osimart customers into local Django users.

Usage:
  # Pull new Osimart customers into the local DB:
  python manage.py sync_customers_from_osimart

  # Also remove local users whose email no longer exists on Osimart:
  python manage.py sync_customers_from_osimart --cleanup

  # Preview what --cleanup would do:
  python manage.py sync_customers_from_osimart --cleanup --dry-run
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from services.osimart import OsimartClient, OsimartError
from website.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Pull all Osimart customers and create local Django users for any that don't exist yet."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be done without creating any users")
        parser.add_argument("--cleanup", action="store_true", help="Delete local non-staff users whose email no longer exists on Osimart")

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        cleanup = options.get("cleanup", False)

        try:
            client = OsimartClient()
        except Exception as e:
            self.stderr.write(f"Failed to initialize OsimartClient: {e}")
            return

        # ---- Step 1: Fetch ALL Osimart customers ----
        self.stdout.write("Fetching Osimart customers...")
        osimart_emails = set()
        osimart_by_email = {}
        page = 1
        fetch_errors = 0
        while True:
            try:
                data = client.get_customers(params={"page": page, "limit": 100})
            except OsimartError as e:
                self.stderr.write(f"Failed to fetch page {page}: {e}")
                fetch_errors += 1
                if fetch_errors > 3:
                    self.stderr.write("Too many fetch errors, aborting.")
                    return
                page += 1
                continue

            if isinstance(data, dict):
                results = data.get("results") or []
            elif isinstance(data, list):
                results = data
            else:
                self.stderr.write(f"Unexpected response format on page {page}")
                break

            if not results:
                break

            for cust in results:
                email = (cust.get("email") or "").strip().lower()
                if email:
                    osimart_emails.add(email)
                    osimart_by_email[email] = cust

            if isinstance(data, dict) and not data.get("next"):
                break

            page += 1

        self.stdout.write(f"Found {len(osimart_emails)} customer(s) on Osimart.")

        # ---- Step 2: Create local users for Osimart customers that don't exist yet ----
        created = 0
        skipped = 0
        errors = []

        for email in osimart_emails:
            existing_user = User.objects.filter(email__iexact=email).first()
            if existing_user:
                cust = osimart_by_email.get(email)
                if cust and not getattr(existing_user.profile, 'osimart_customer_id', None):
                    existing_user.profile.osimart_customer_id = str(cust.get("id", ""))
                    existing_user.profile.save(update_fields=["osimart_customer_id"])
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(f"  WOULD CREATE {email}")
                created += 1
                continue

            try:
                osimart_customer_id = osimart_by_email.get(email, {}).get("id", "")
                user = User.objects.create_user(
                    username=email,
                    email=email,
                )
                user.set_unusable_password()
                user.save()
                UserProfile.objects.create(user=user, osimart_customer_id=str(osimart_customer_id))
                self.stdout.write(f"  OK   {email}")
                created += 1
            except Exception as e:
                # username collision — append random suffix
                try:
                    from uuid import uuid4
                    user = User.objects.create_user(
                        username=email.split("@")[0] + "_" + uuid4().hex[:6],
                        email=email,
                    )
                    user.set_unusable_password()
                    user.save()
                    UserProfile.objects.create(user=user, osimart_customer_id=str(osimart_customer_id))
                    self.stdout.write(f"  OK   {email} (alt username)")
                    created += 1
                except Exception as e2:
                    self.stderr.write(f"  ERROR {email}: {e2}")
                    errors.append(email)

        label = "Would create" if dry_run else "Created"
        self.stdout.write(f"\nImport done. {label}: {created}, Skipped: {skipped}, Errors: {len(errors)}")

        # ---- Step 3: Cleanup local users no longer on Osimart (optional --cleanup) ----
        if not cleanup:
            return

        self.stdout.write("\n--- Cleanup phase ---")
        local_users = User.objects.filter(is_staff=False)
        deleted = 0
        cleanup_errors = []

        for user in local_users:
            if not user.email:
                continue
            email_lower = user.email.strip().lower()
            if email_lower in osimart_emails:
                continue

            if dry_run:
                self.stdout.write(f"  WOULD DELETE {user.email} (user #{user.id})")
                deleted += 1
                continue

            try:
                user.delete()
                self.stdout.write(f"  DELETED {email_lower}")
                deleted += 1
            except Exception as e:
                self.stderr.write(f"  ERROR deleting {email_lower}: {e}")
                cleanup_errors.append(email_lower)

        cl_label = "Would delete" if dry_run else "Deleted"
        self.stdout.write(f"Cleanup done. {cl_label}: {deleted}, Errors: {len(cleanup_errors)}")
        if cleanup_errors:
            self.stderr.write(f"Cleanup errors: {', '.join(cleanup_errors)}")
