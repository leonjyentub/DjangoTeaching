from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create/update the Authors group with article add/change/view permissions."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            nargs="*",
            default=[],
            help="Optional usernames to add to the Authors group.",
        )

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Authors")
        permissions = Permission.objects.filter(
            content_type__app_label="journal",
            codename__in=["add_article", "change_article", "view_article"],
        )
        if permissions.count() != 3:
            raise CommandError("Article permissions are missing. Run migrations first.")
        group.permissions.set(permissions)

        usernames = options["users"]
        if usernames:
            from django.contrib.auth import get_user_model

            User = get_user_model()
            found = {user.username: user for user in User.objects.filter(username__in=usernames)}
            missing = sorted(set(usernames) - set(found))
            if missing:
                raise CommandError(f"Unknown username(s): {', '.join(missing)}")
            for username in usernames:
                found[username].groups.add(group)

        self.stdout.write(self.style.SUCCESS("Authors group is ready."))
