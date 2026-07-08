"""Pull all Osimart customers into local Django users."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from services.osimart import OsimartClient, OsimartError

User = get_user_model()


class Command(BaseCommand):
    help = "Pull all Osimart customers and create local Django users for any that don't exist yet."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be done without creating any users")

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)

        try:
            client = OsimartClient()
        except Exception as e:
            self.stderr.write(f"Failed to initialize OsimartClient: {e}")
            return

        created = 0
        skipped = 0
        errors = []

        page = 1
        while True:
            try:
                data = client.get_customers(params={"page": page, "limit": 100})
            except OsimartError as e:
                self.stderr.write(f"Failed to fetch page {page}: {e}")
                errors.append(f"page_{page}")
                break

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
                first_name = (cust.get("first_name") or "").strip()
                last_name = (cust.get("last_name") or "").strip()
                username = email or cust.get("id", "")

                if not email:
                    self.stdout.write(f"  SKIP customer {cust.get('id')}: no email")
                    skipped += 1
                    continue

                if User.objects.filter(email=email).exists():
                    self.stdout.write(f"  SKIP {email}: local user already exists")
                    skipped += 1
                    continue

                if dry_run:
                    self.stdout.write(f"  WOULD CREATE {email} ({first_name} {last_name})")
                    created += 1
                    continue

                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    user.set_unusable_password()
                    user.save()
                    self.stdout.write(f"  OK   {email} ({first_name} {last_name})")
                    created += 1
                except Exception as e:
                    self.stderr.write(f"  ERROR {email}: {e}")
                    errors.append(email)

            if isinstance(data, dict) and not data.get("next"):
                break

            page += 1

        label = "Would create" if dry_run else "Created"
        self.stdout.write(f"\nDone. {label}: {created}, Skipped: {skipped}, Errors: {len(errors)}")
        if errors:
            self.stderr.write(f"Errors: {', '.join(errors)}")
