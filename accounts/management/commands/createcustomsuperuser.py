"""
Extend createsuperuser command to allow non-interactive creation of a
superuser with a password.
Example usage:
  ./manage.py createcustomsuperuser --password foo --email foo@bar
"""
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        return user


def create_user(email, password):
    return User.objects.create_superuser(email=email, password=password)


class Command(createsuperuser.Command):
    help = 'Create a superuser with a password non-interactively'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        password = options.get('password')
        email = options.get('email')
        if not password or not email:
            raise CommandError("--email and --password are required options")
        if get_user(email) and options.get('verbosity', 0):
            self.stdout.write(
                'User with email "{}" already exists'.format(email))
            return
        user = create_user(email, password)
        if user and options.get('verbosity', 0):
            self.stdout.write(
                'Superuser with email "{}" created'.format(email))
