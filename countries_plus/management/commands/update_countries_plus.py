from django.core.management.base import BaseCommand

from countries_plus.utils import update_geonames_data


class Command(BaseCommand):
    help = 'Updates the Countries Plus database from geonames.org'

    def handle(self, *args, **options):
        num_updated, num_created = update_geonames_data()
        self.stdout.write(
            "Countries Plus data has been successfully updated from geonames.org.  "
            "%s countries were updated, %s countries were created."
            % (num_updated, num_created)
        )
