from django.db import models


class Vehicle(models.Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    ]

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )

    vehicle_type = models.CharField(
        max_length=50
    )

    driver = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='offline'
    )

    speed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    last_update = models.DateTimeField(
        auto_now=True
    )

    gps_last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.registration_number


class VehicleLocation(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='location_history'
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7
    )

    speed = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.recorded_at}'
        )
class MaintenanceRecord(models.Model):

    MAINTENANCE_TYPE_CHOICES = [
        ('service', 'Routine Service'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('tyres', 'Tyres'),
        ('oil_change', 'Oil Change'),
        ('brakes', 'Brakes'),
        ('electrical', 'Electrical'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )

    maintenance_type = models.CharField(
        max_length=30,
        choices=MAINTENANCE_TYPE_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    service_date = models.DateField()

    next_service_date = models.DateField(
        null=True,
        blank=True
    )

    mileage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    service_provider = models.CharField(
        max_length=150,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.get_maintenance_type_display()} - '
            f'{self.service_date}'
        )

class FuelRecord(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='fuel_records'
    )

    fuel_date = models.DateField()

    litres = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    mileage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    fuel_station = models.CharField(
        max_length=150,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.fuel_date}'
        )

class Driver(models.Model):

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    license_number = models.CharField(
        max_length=50,
        blank=True
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_drivers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

class Alert(models.Model):

    ALERT_TYPE_CHOICES = [
        ('overspeed', 'Overspeed'),
        ('offline', 'Vehicle Offline'),
        ('maintenance', 'Maintenance Due'),
    ]

    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='alerts'
    )

    alert_type = models.CharField(
        max_length=30,
        choices=ALERT_TYPE_CHOICES
    )

    message = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='unread'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.get_alert_type_display()}'
        )

class VehicleDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ('insurance', 'Insurance'),
        ('logbook', 'Logbook'),
        ('inspection', 'Inspection Certificate'),
        ('licence', 'Road Licence'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES
    )

    document_number = models.CharField(
        max_length=100,
        blank=True
    )

    issue_date = models.DateField(
        null=True,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.get_document_type_display()}'
        )

class Trip(models.Model):

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='trips'
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trips'
    )

    start_location = models.CharField(
        max_length=200
    )

    destination = models.CharField(
        max_length=200
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.start_location} to '
            f'{self.destination}'
        )

class Expense(models.Model):

    EXPENSE_TYPE_CHOICES = [
        ('insurance', 'Insurance'),
        ('parking', 'Parking'),
        ('toll', 'Toll'),
        ('repair', 'Repair'),
        ('tyres', 'Tyres'),
        ('parts', 'Spare Parts'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    expense_type = models.CharField(
        max_length=30,
        choices=EXPENSE_TYPE_CHOICES
    )

    expense_date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f'{self.vehicle.registration_number} - '
            f'{self.get_expense_type_display()} - '
            f'{self.expense_date}'
        )

class FleetSetting(models.Model):

    fleet_name = models.CharField(
        max_length=150,
        default='My Fleet'
    )

    currency = models.CharField(
        max_length=10,
        default='KES'
    )

    default_speed_limit = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=80
    )

    contact_phone = models.CharField(
        max_length=30,
        blank=True
    )

    contact_email = models.EmailField(
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.fleet_name

class CRMActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Call'),
        ('email', 'Email'),
        ('inquiry', 'Inquiry'),
        ('follow_up', 'Follow-up'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]

    client_name = models.CharField(max_length=150)
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPE_CHOICES
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    activity_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} - {self.get_activity_type_display()}'


class SupportTicket(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    issue = models.CharField(max_length=200)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='support_tickets'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.issue} - {self.get_priority_display()}'
