from django import forms

from .models import (
    Vehicle,
    MaintenanceRecord,
    FuelRecord,
    Driver,
    Alert,
    VehicleDocument,
    Trip,
    Expense,
    FleetSetting,
    CRMActivity,
    SupportTicket
)


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        fields = [
            'registration_number',
            'vehicle_type',
            'driver',
            'status',
            'speed',
            'location',
        ]

        widgets = {
            'registration_number': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. KDA 001A'
                }
            ),

            'vehicle_type': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Truck, Van, Pickup'
                }
            ),

            'driver': forms.TextInput(
                attrs={
                    'placeholder': 'Driver name'
                }
            ),

            'status': forms.Select(),

            'speed': forms.NumberInput(
                attrs={
                    'placeholder': '0',
                    'step': '0.01'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Nairobi'
                }
            ),
        }


class MaintenanceRecordForm(forms.ModelForm):

    class Meta:
        model = MaintenanceRecord

        fields = [
            'vehicle',
            'maintenance_type',
            'description',
            'service_date',
            'next_service_date',
            'mileage',
            'cost',
            'service_provider',
            'status',
            'notes',
        ]

        widgets = {
            'vehicle': forms.Select(),

            'maintenance_type': forms.Select(),

            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Describe the maintenance work'
                }
            ),

            'service_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'next_service_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'mileage': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'e.g. 125000'
                }
            ),

            'cost': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'e.g. 15000'
                }
            ),

            'service_provider': forms.TextInput(
                attrs={
                    'placeholder': 'Garage or service provider'
                }
            ),

            'status': forms.Select(),

            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }

class FuelRecordForm(forms.ModelForm):

    class Meta:
        model = FuelRecord

        fields = [
            'vehicle',
            'fuel_date',
            'litres',
            'cost',
            'mileage',
            'fuel_station',
            'notes',
        ]

        widgets = {
            'fuel_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'litres': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'e.g. 50'
                }
            ),
            'cost': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'e.g. 8000'
                }
            ),
            'mileage': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'e.g. 125000'
                }
            ),
            'fuel_station': forms.TextInput(
                attrs={
                    'placeholder': 'Fuel station'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }

class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver

        fields = [
            'name',
            'phone',
            'license_number',
            'vehicle',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Driver name'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Phone number'
                }
            ),
            'license_number': forms.TextInput(
                attrs={
                    'placeholder': 'Driving license number'
                }
            ),
            'vehicle': forms.Select(),
        }

class AlertForm(forms.ModelForm):

    class Meta:
        model = Alert

        fields = [
            'vehicle',
            'alert_type',
            'message',
            'status',
        ]

        widgets = {
            'message': forms.TextInput(
                attrs={
                    'placeholder': 'Enter alert message'
                }
            ),
        }

class VehicleDocumentForm(forms.ModelForm):

    class Meta:
        model = VehicleDocument

        fields = [
            'vehicle',
            'document_type',
            'document_number',
            'issue_date',
            'expiry_date',
            'notes',
        ]

        widgets = {
            'issue_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'expiry_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'document_number': forms.TextInput(
                attrs={
                    'placeholder': 'Document number'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip

        fields = [
            'vehicle',
            'driver',
            'start_location',
            'destination',
            'start_time',
            'end_time',
            'distance',
            'status',
            'notes',
        ]

        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),

            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                }
            ),

            'start_location': forms.TextInput(
                attrs={
                    'placeholder': 'Starting location'
                }
            ),

            'destination': forms.TextInput(
                attrs={
                    'placeholder': 'Destination'
                }
            ),

            'distance': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'Distance in km'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'vehicle',
            'expense_type',
            'expense_date',
            'amount',
            'description',
            'notes',
        ]

        widgets = {
            'expense_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'Amount'
                }
            ),

            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Expense description'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }

class FleetSettingForm(forms.ModelForm):

    class Meta:

        model = FleetSetting

        fields = [
            'fleet_name',
            'currency',
            'default_speed_limit',
            'contact_phone',
            'contact_email',
            'address',
        ]

        widgets = {

            'fleet_name': forms.TextInput(
                attrs={
                    'placeholder': 'Fleet name'
                }
            ),

            'currency': forms.TextInput(
                attrs={
                    'placeholder': 'KES'
                }
            ),

            'default_speed_limit': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'placeholder': 'Default speed limit'
                }
            ),

            'contact_phone': forms.TextInput(
                attrs={
                    'placeholder': 'Contact phone'
                }
            ),

            'contact_email': forms.EmailInput(
                attrs={
                    'placeholder': 'Contact email'
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Fleet address'
                }
            ),
        }

class CRMActivityForm(forms.ModelForm):
    class Meta:
        model = CRMActivity
        fields = [
            'client_name',
            'activity_type',
            'description',
            'status',
            'activity_date',
            'notes',
        ]
        widgets = {
            'client_name': forms.TextInput(
                attrs={'placeholder': 'Client name'}
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Describe the customer activity'
                }
            ),
            'activity_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = [
            'issue',
            'vehicle',
            'priority',
            'status',
            'description',
            'notes',
        ]
        widgets = {
            'issue': forms.TextInput(
                attrs={'placeholder': 'Support issue'}
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Describe the issue'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Additional notes'
                }
            ),
        }