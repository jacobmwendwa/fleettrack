import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from dashboard.models import Vehicle, VehicleLocation


class Command(BaseCommand):

    help = 'Simulate GPS updates for a vehicle'

    def add_arguments(self, parser):

        parser.add_argument(
            '--vehicle',
            type=str,
            required=True,
            help='Vehicle registration number'
        )

    def handle(self, *args, **options):

        registration = options['vehicle']

        try:
            vehicle = Vehicle.objects.get(
                registration_number=registration
            )

        except Vehicle.DoesNotExist:

            self.stdout.write(
                self.style.ERROR(
                    f'Vehicle {registration} was not found.'
                )
            )

            return

        self.stdout.write(
            self.style.SUCCESS(
                f'Starting GPS simulation for {registration}'
            )
        )

        latitude = float(
            vehicle.latitude or -1.286389
        )

        longitude = float(
            vehicle.longitude or 36.817223
        )

        speed = 60.0

        while True:

            # Move the vehicle
            latitude += 0.0002
            longitude += 0.0002

            # Change speed
            speed += 1

            if speed > 80:
                speed = 60

            # Update current vehicle position
            vehicle.latitude = latitude
            vehicle.longitude = longitude
            vehicle.speed = speed
            vehicle.gps_last_seen = timezone.now()
            vehicle.status = 'active'

            vehicle.save()

            # Save GPS position to history
            VehicleLocation.objects.create(
                vehicle=vehicle,
                latitude=latitude,
                longitude=longitude,
                speed=speed
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'{vehicle.registration_number} | '
                    f'Lat: {latitude:.6f} | '
                    f'Lng: {longitude:.6f} | '
                    f'Speed: {speed:.1f} km/h | '
                    f'GPS history saved'
                )
            )

            time.sleep(10)