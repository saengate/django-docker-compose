from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'DOES SOMETHING.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            '¡Termino la tarea!',
        ))
