from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2
from django.db.models import Avg, Max, Count
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse

from .models import (
    Vehicle,
    VehicleLocation,
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
from .forms import (
    VehicleForm,
    MaintenanceRecordForm,
    FuelRecordForm,
    DriverForm,
    AlertForm,
    VehicleDocumentForm,
    TripForm,
    ExpenseForm,
    FleetSettingForm,
    CRMActivityForm,
    SupportTicketForm
)


@login_required
def dashboard_home(request):
    total_vehicles = Vehicle.objects.count()

    active_vehicles = Vehicle.objects.filter(
        status='active'
    ).count()

    offline_vehicles = Vehicle.objects.filter(
        status='offline'
    ).count()

    maintenance_vehicles = Vehicle.objects.filter(
        status='maintenance'
    ).count()

    active_trips = Trip.objects.filter(
        status='in_progress'
    ).count()

    completed_trips = Trip.objects.filter(
        status='completed'
    ).count()

    unread_alerts = Alert.objects.filter(
        status='unread'
    ).count()

    total_fuel_cost = FuelRecord.objects.aggregate(
        total=Sum('cost')
    )['total'] or 0

    total_maintenance_cost = MaintenanceRecord.objects.aggregate(
        total=Sum('cost')
    )['total'] or 0

    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    recent_alerts = Alert.objects.select_related(
        'vehicle'
    ).order_by('-created_at')[:5]

    recent_trips = Trip.objects.select_related(
        'vehicle',
        'driver'
    ).order_by('-start_time')[:5]

    recent_crm_activity = CRMActivity.objects.order_by(
        '-activity_date',
        '-created_at'
    )[:5]

    open_support_tickets = SupportTicket.objects.select_related(
        'vehicle'
    ).exclude(
        status='resolved'
    ).order_by('-created_at')[:5]

    context = {
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'offline_vehicles': offline_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'active_trips': active_trips,
        'completed_trips': completed_trips,
        'unread_alerts': unread_alerts,
        'total_fuel_cost': total_fuel_cost,
        'total_maintenance_cost': total_maintenance_cost,
        'total_expenses': total_expenses,
        'recent_alerts': recent_alerts,
        'recent_trips': recent_trips,
        'recent_crm_activity': recent_crm_activity,
        'open_support_tickets': open_support_tickets,
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@login_required
def reports(request):

    # Vehicle summary
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    offline_vehicles = Vehicle.objects.filter(status='offline').count()
    maintenance_vehicles = Vehicle.objects.filter(status='maintenance').count()

    # Fuel summary
    total_fuel_litres = FuelRecord.objects.aggregate(
        total=Sum('litres')
    )['total'] or 0

    total_fuel_cost = FuelRecord.objects.aggregate(
        total=Sum('cost')
    )['total'] or 0

    # Maintenance summary
    total_maintenance_records = MaintenanceRecord.objects.count()

    total_maintenance_cost = MaintenanceRecord.objects.aggregate(
        total=Sum('cost')
    )['total'] or 0

    # Trip summary
    total_trips = Trip.objects.count()

    completed_trips = Trip.objects.filter(
        status='completed'
    ).count()

    total_distance = Trip.objects.aggregate(
        total=Sum('distance')
    )['total'] or 0

    # Expense summary
    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'offline_vehicles': offline_vehicles,
        'maintenance_vehicles': maintenance_vehicles,

        'total_fuel_litres': total_fuel_litres,
        'total_fuel_cost': total_fuel_cost,

        'total_maintenance_records': total_maintenance_records,
        'total_maintenance_cost': total_maintenance_cost,

        'total_trips': total_trips,
        'completed_trips': completed_trips,
        'total_distance': total_distance,

        'total_expenses': total_expenses,
    }

    return render(
        request,
        'dashboard/reports.html',
        context
    )

@login_required
def vehicles(request):

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    vehicle_list = Vehicle.objects.all()

    if search:
        vehicle_list = vehicle_list.filter(
            Q(registration_number__icontains=search) |
            Q(vehicle_type__icontains=search) |
            Q(driver__icontains=search) |
            Q(location__icontains=search)
        )

    if status:
        vehicle_list = vehicle_list.filter(
            status=status
        )

    vehicle_list = vehicle_list.order_by(
        'registration_number'
    )

    context = {
        'vehicles': vehicle_list,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'dashboard/vehicles.html',
        context
    )


@login_required
def add_vehicle(request):

    if request.method == 'POST':

        form = VehicleForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('vehicles')

    else:

        form = VehicleForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_vehicle.html',
        context
    )


@login_required
def vehicle_detail(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    context = {
        'vehicle': vehicle,
    }

    return render(
        request,
        'dashboard/vehicle_detail.html',
        context
    )


@login_required
def edit_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    if request.method == 'POST':

        form = VehicleForm(
            request.POST,
            instance=vehicle
        )

        if form.is_valid():

            form.save()

            return redirect(
                'vehicle_detail',
                vehicle_id=vehicle.id
            )

    else:

        form = VehicleForm(
            instance=vehicle
        )

    context = {
        'form': form,
        'vehicle': vehicle,
    }

    return render(
        request,
        'dashboard/edit_vehicle.html',
        context
    )


@login_required
def delete_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    if request.method == 'POST':

        vehicle.delete()

        return redirect('vehicles')

    context = {
        'vehicle': vehicle,
    }

    return render(
        request,
        'dashboard/delete_vehicle.html',
        context
    )

@login_required
def live_tracking(request):

    vehicle_list = Vehicle.objects.exclude(
        latitude__isnull=True
    ).exclude(
        longitude__isnull=True
    ).order_by(
        'registration_number'
    )

    now = timezone.now()

    for vehicle in vehicle_list:

        if vehicle.status == 'maintenance':
            vehicle.tracking_status = 'maintenance'

        elif vehicle.gps_last_seen:

            time_since_update = (
                now - vehicle.gps_last_seen
            )

            if time_since_update <= timedelta(minutes=5):
                vehicle.tracking_status = 'online'
            else:
                vehicle.tracking_status = 'offline'

        else:
            vehicle.tracking_status = 'offline'

    context = {
        'vehicles': vehicle_list,
    }

    return render(
        request,
        'dashboard/live_tracking.html',
        context
    )

@login_required
def update_vehicle_location(request, vehicle_id):

    if request.method != 'POST':
        return JsonResponse(
            {
                'success': False,
                'message': 'Only POST requests are allowed.'
            },
            status=405
        )

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    try:
        latitude = float(
            request.POST.get('latitude')
        )

        longitude = float(
            request.POST.get('longitude')
        )

        speed = float(
            request.POST.get('speed', 0)
        )

    except (TypeError, ValueError):

        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid GPS data.'
            },
            status=400
        )

    # Update the vehicle's current GPS position
    vehicle.latitude = latitude
    vehicle.longitude = longitude
    vehicle.speed = speed
    vehicle.gps_last_seen = timezone.now()

    vehicle.save()

    # Save GPS position to historical records
    VehicleLocation.objects.create(
        vehicle=vehicle,
        latitude=latitude,
        longitude=longitude,
        speed=speed
    )

    return JsonResponse(
        {
            'success': True,
            'vehicle': vehicle.registration_number,
            'latitude': float(vehicle.latitude),
            'longitude': float(vehicle.longitude),
            'speed': float(vehicle.speed),
            'gps_last_seen': (
                vehicle.gps_last_seen.isoformat()
            ),
        }
    )
@login_required
def vehicle_locations_api(request):

    vehicles = Vehicle.objects.exclude(
        latitude__isnull=True
    ).exclude(
        longitude__isnull=True
    ).order_by(
        'registration_number'
    )

    now = timezone.now()

    vehicle_data = []

    for vehicle in vehicles:

        if vehicle.status == 'maintenance':

            tracking_status = 'maintenance'

        elif vehicle.gps_last_seen:

            time_since_update = (
                now - vehicle.gps_last_seen
            )

            if time_since_update <= timedelta(minutes=5):
                tracking_status = 'online'
            else:
                tracking_status = 'offline'

        else:

            tracking_status = 'offline'

        vehicle_data.append({
            'id': vehicle.id,
            'registration': vehicle.registration_number,
            'driver': vehicle.driver or 'Not Assigned',
            'status': vehicle.status,
            'tracking_status': tracking_status,
            'speed': float(vehicle.speed),
            'location': vehicle.location or 'Unknown',
            'latitude': float(vehicle.latitude),
            'longitude': float(vehicle.longitude),
            'gps_last_seen': (
                vehicle.gps_last_seen.isoformat()
                if vehicle.gps_last_seen
                else None
            ),
        })

    return JsonResponse({
        'success': True,
        'vehicles': vehicle_data,
    })

@login_required
def vehicle_history(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    history = list(
        VehicleLocation.objects.filter(
            vehicle=vehicle
        ).order_by(
            'recorded_at'
        )
    )

    total_points = len(history)

    total_distance = 0.0

    average_speed = 0.0
    maximum_speed = 0.0
    trip_duration = None

    if history:

        speeds = [
            float(record.speed)
            for record in history
        ]

        average_speed = (
            sum(speeds) / len(speeds)
        )

        maximum_speed = max(speeds)

    if len(history) >= 2:

        first_record = history[0]
        last_record = history[-1]

        trip_duration = (
            last_record.recorded_at -
            first_record.recorded_at
        )

        earth_radius_km = 6371.0

        for index in range(1, len(history)):

            previous = history[index - 1]
            current = history[index]

            lat1 = radians(
                float(previous.latitude)
            )

            lon1 = radians(
                float(previous.longitude)
            )

            lat2 = radians(
                float(current.latitude)
            )

            lon2 = radians(
                float(current.longitude)
            )

            delta_lat = lat2 - lat1
            delta_lon = lon2 - lon1

            a = (
                sin(delta_lat / 2) ** 2
                +
                cos(lat1)
                *
                cos(lat2)
                *
                sin(delta_lon / 2) ** 2
            )

            c = 2 * atan2(
                sqrt(a),
                sqrt(1 - a)
            )

            distance = earth_radius_km * c

            total_distance += distance

    context = {
        'vehicle': vehicle,
        'history': history,
        'total_points': total_points,
        'total_distance': total_distance,
        'average_speed': average_speed,
        'maximum_speed': maximum_speed,
        'trip_duration': trip_duration,
    }

    return render(
        request,
        'dashboard/vehicle_history.html',
        context
    )

@login_required
def fleet_analytics(request):

    period = request.GET.get(
        'period',
        'all'
    )

    now = timezone.now()

    if period == 'today':

        start_date = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif period == '7days':

        start_date = now - timedelta(days=7)

    elif period == '30days':

        start_date = now - timedelta(days=30)

    else:

        start_date = None

    # =================================
    # VEHICLE STATUS
    # =================================

    vehicles = Vehicle.objects.all().order_by(
        'registration_number'
    )

    total_vehicles = vehicles.count()

    active_vehicles = vehicles.filter(
        status='active'
    ).count()

    offline_vehicles = vehicles.filter(
        status='offline'
    ).count()

    maintenance_vehicles = vehicles.filter(
        status='maintenance'
    ).count()

    # =================================
    # GPS RECORDS
    # =================================

    gps_records = VehicleLocation.objects.all()

    if start_date:

        gps_records = gps_records.filter(
            recorded_at__gte=start_date
        )

    total_gps_records = gps_records.count()

    average_fleet_speed = (
        gps_records.aggregate(
            average=Avg('speed')
        )['average'] or 0
    )

    maximum_fleet_speed = (
        gps_records.aggregate(
            maximum=Max('speed')
        )['maximum'] or 0
    )

    # =================================
    # OVERSPEED
    # =================================

    overspeed_threshold = 80

    overspeed_records = gps_records.filter(
        speed__gt=overspeed_threshold
    ).count()

    # =================================
    # VEHICLE STATISTICS
    # =================================

    vehicle_statistics = []

    for vehicle in vehicles:

        records = VehicleLocation.objects.filter(
            vehicle=vehicle
        ).order_by(
            'recorded_at'
        )

        if start_date:

            records = records.filter(
                recorded_at__gte=start_date
            )

        records = list(records)

        # Distance
        total_distance = 0.0

        if len(records) >= 2:

            earth_radius_km = 6371.0

            for index in range(1, len(records)):

                previous = records[index - 1]
                current = records[index]

                lat1 = radians(
                    float(previous.latitude)
                )

                lon1 = radians(
                    float(previous.longitude)
                )

                lat2 = radians(
                    float(current.latitude)
                )

                lon2 = radians(
                    float(current.longitude)
                )

                delta_lat = lat2 - lat1
                delta_lon = lon2 - lon1

                a = (
                    sin(delta_lat / 2) ** 2
                    +
                    cos(lat1)
                    * cos(lat2)
                    * sin(delta_lon / 2) ** 2
                )

                c = 2 * atan2(
                    sqrt(a),
                    sqrt(1 - a)
                )

                total_distance += (
                    earth_radius_km * c
                )

        # Average speed
        vehicle_average_speed = (
            sum(
                float(record.speed)
                for record in records
            ) / len(records)
            if records
            else 0
        )

        # Maximum speed
        vehicle_maximum_speed = max(
            (
                float(record.speed)
                for record in records
            ),
            default=0
        )

        # Overspeed events
        vehicle_overspeed = sum(
            1
            for record in records
            if float(record.speed) > overspeed_threshold
        )

        # Overspeed percentage
        overspeed_percentage = (
            (
                vehicle_overspeed
                / len(records)
            ) * 100
            if records
            else 0
        )

        vehicle_statistics.append({
            'vehicle': vehicle,
            'gps_records': len(records),
            'distance': total_distance,
            'average_speed': vehicle_average_speed,
            'maximum_speed': vehicle_maximum_speed,
            'overspeed_events': vehicle_overspeed,
            'overspeed_percentage': overspeed_percentage,
        })

    # =================================
    # FLEET STATUS CHART
    # =================================

    status_chart = {
        'active': active_vehicles,
        'offline': offline_vehicles,
        'maintenance': maintenance_vehicles,
    }

    # =================================
    # OVERSPEED CHART
    # =================================

    overspeed_chart = []

    for item in vehicle_statistics:

        overspeed_chart.append({
            'registration': (
                item['vehicle'].registration_number
            ),
            'overspeed_events': (
                item['overspeed_events']
            ),
        })

    # =================================
    # OVERSPEED ALERTS
    # =================================

    overspeed_alerts = []

    for item in vehicle_statistics:

        if item['overspeed_events'] > 0:

            maximum_speed = item['maximum_speed']

            if maximum_speed > 100:

                severity = 'critical'

            elif maximum_speed > 90:

                severity = 'high'

            else:

                severity = 'moderate'

            overspeed_alerts.append({
                'vehicle_id': item['vehicle'].id,
                'registration': (
                    item['vehicle'].registration_number
                ),
                'driver': (
                    item['vehicle'].driver
                ),
                'overspeed_events': (
                    item['overspeed_events']
                ),
                'overspeed_percentage': (
                    item['overspeed_percentage']
                ),
                'maximum_speed': maximum_speed,
                'severity': severity,
            })

    # =================================
    # DAILY GPS ACTIVITY
    # =================================

    daily_records = (
        gps_records
        .annotate(
            day=TruncDate('recorded_at')
        )
        .values('day')
        .annotate(
            records=Count('id'),
            average_speed=Avg('speed')
        )
        .order_by('day')
    )

    activity_chart = []

    for item in daily_records:

        activity_chart.append({
            'day': item['day'].strftime('%d %b'),
            'records': item['records'],
            'average_speed': round(
                float(
                    item['average_speed'] or 0
                ),
                2
            ),
        })

    # =================================
    # DISTANCE CHART
    # =================================

    distance_chart = []

    for item in vehicle_statistics:

        distance_chart.append({
            'registration': (
                item['vehicle'].registration_number
            ),
            'distance': round(
                item['distance'],
                2
            ),
        })

    # =================================
    # CONTEXT
    # =================================

    context = {
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'offline_vehicles': offline_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'total_gps_records': total_gps_records,
        'average_fleet_speed': average_fleet_speed,
        'maximum_fleet_speed': maximum_fleet_speed,
        'overspeed_records': overspeed_records,
        'vehicle_statistics': vehicle_statistics,
        'status_chart': status_chart,
        'distance_chart': distance_chart,
        'activity_chart': activity_chart,
        'overspeed_chart': overspeed_chart,
        'overspeed_alerts': overspeed_alerts,
        'period': period,
        'overspeed_threshold': overspeed_threshold,
    }

    return render(
        request,
        'dashboard/fleet_analytics.html',
        context
    )

@login_required
def maintenance_records(request):

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    maintenance_list = MaintenanceRecord.objects.select_related(
        'vehicle'
    ).all()

    if search:

        maintenance_list = maintenance_list.filter(
            Q(vehicle__registration_number__icontains=search) |
            Q(description__icontains=search) |
            Q(service_provider__icontains=search) |
            Q(notes__icontains=search)
        )

    if status:

        maintenance_list = maintenance_list.filter(
            status=status
        )

    maintenance_list = maintenance_list.order_by(
        '-service_date'
    )

    context = {
        'maintenance_records': maintenance_list,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'dashboard/maintenance.html',
        context
    )


@login_required
def add_maintenance(request):

    if request.method == 'POST':

        form = MaintenanceRecordForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'maintenance_records'
            )

    else:

        form = MaintenanceRecordForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_maintenance.html',
        context
    )

@login_required
def fuel_records(request):

    search = request.GET.get('search', '').strip()

    fuel_list = FuelRecord.objects.select_related(
        'vehicle'
    ).all()

    if search:

        fuel_list = fuel_list.filter(
            Q(vehicle__registration_number__icontains=search) |
            Q(fuel_station__icontains=search) |
            Q(notes__icontains=search)
        )

    fuel_list = fuel_list.order_by('-fuel_date')

    context = {
        'fuel_records': fuel_list,
        'search': search,
    }

    return render(
        request,
        'dashboard/fuel.html',
        context
    )


@login_required
def add_fuel(request):

    if request.method == 'POST':

        form = FuelRecordForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'fuel_records'
            )

    else:

        form = FuelRecordForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_fuel.html',
        context
    )

@login_required
def drivers(request):

    search = request.GET.get('search', '').strip()

    driver_list = Driver.objects.select_related(
        'vehicle'
    ).all()

    if search:

        driver_list = driver_list.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(license_number__icontains=search) |
            Q(vehicle__registration_number__icontains=search)
        )

    driver_list = driver_list.order_by('name')

    context = {
        'drivers': driver_list,
        'search': search,
    }

    return render(
        request,
        'dashboard/drivers.html',
        context
    )


@login_required
def add_driver(request):

    if request.method == 'POST':

        form = DriverForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'drivers'
            )

    else:

        form = DriverForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_driver.html',
        context
    )

@login_required
def edit_driver(request, driver_id):

    driver = get_object_or_404(
        Driver,
        id=driver_id
    )

    if request.method == 'POST':

        form = DriverForm(
            request.POST,
            instance=driver
        )

        if form.is_valid():

            form.save()

            return redirect(
                'drivers'
            )

    else:

        form = DriverForm(
            instance=driver
        )

    context = {
        'form': form,
        'driver': driver,
    }

    return render(
        request,
        'dashboard/edit_driver.html',
        context
    )

@login_required
def delete_driver(request, driver_id):

    driver = get_object_or_404(
        Driver,
        id=driver_id
    )

    if request.method == 'POST':

        driver.delete()

        return redirect(
            'drivers'
        )

    context = {
        'driver': driver,
    }

    return render(
        request,
        'dashboard/delete_driver.html',
        context
    )

@login_required
def alerts(request):

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    alert_list = Alert.objects.select_related(
        'vehicle'
    ).all()

    if search:

        alert_list = alert_list.filter(
            Q(vehicle__registration_number__icontains=search) |
            Q(message__icontains=search)
        )

    if status:

        alert_list = alert_list.filter(
            status=status
        )

    alert_list = alert_list.order_by('-created_at')

    context = {
        'alerts': alert_list,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'dashboard/alerts.html',
        context
    )


@login_required
def add_alert(request):

    if request.method == 'POST':

        form = AlertForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'alerts'
            )

    else:

        form = AlertForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_alert.html',
        context
    )
@login_required
def mark_alert_read(request, alert_id):

    alert = get_object_or_404(
        Alert,
        id=alert_id
    )

    alert.status = 'read'
    alert.save()

    return redirect(
        'alerts'
    )
@login_required
def delete_alert(request, alert_id):

    alert = get_object_or_404(
        Alert,
        id=alert_id
    )

    if request.method == 'POST':

        alert.delete()

        return redirect(
            'alerts'
        )

    context = {
        'alert': alert,
    }

    return render(
        request,
        'dashboard/delete_alert.html',
        context
    )

@login_required
def vehicle_documents(request):

    document_list = VehicleDocument.objects.select_related(
        'vehicle'
    ).order_by(
        '-created_at'
    )

    context = {
        'documents': document_list,
    }

    return render(
        request,
        'dashboard/vehicle_documents.html',
        context
    )


@login_required
def add_vehicle_document(request):

    if request.method == 'POST':

        form = VehicleDocumentForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'vehicle_documents'
            )

    else:

        form = VehicleDocumentForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_vehicle_document.html',
        context
    )

@login_required
def delete_vehicle_document(request, document_id):

    document = get_object_or_404(
        VehicleDocument,
        id=document_id
    )

    if request.method == 'POST':

        document.delete()

        return redirect(
            'vehicle_documents'
        )

    context = {
        'document': document,
    }

    return render(
        request,
        'dashboard/delete_vehicle_document.html',
        context
    )

@login_required
def trips(request):

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    trip_list = Trip.objects.select_related(
        'vehicle',
        'driver'
    ).all()

    if search:

        trip_list = trip_list.filter(
            Q(vehicle__registration_number__icontains=search) |
            Q(driver__name__icontains=search) |
            Q(start_location__icontains=search) |
            Q(destination__icontains=search)
        )

    if status:

        trip_list = trip_list.filter(
            status=status
        )

    trip_list = trip_list.order_by('-start_time')

    context = {
        'trips': trip_list,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'dashboard/trips.html',
        context
    )


@login_required
def add_trip(request):

    if request.method == 'POST':

        form = TripForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'trips'
            )

    else:

        form = TripForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_trip.html',
        context
    )

@login_required
def edit_trip(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id
    )

    if request.method == 'POST':

        form = TripForm(
            request.POST,
            instance=trip
        )

        if form.is_valid():

            form.save()

            return redirect(
                'trips'
            )

    else:

        form = TripForm(
            instance=trip
        )

    context = {
        'form': form,
        'trip': trip,
    }

    return render(
        request,
        'dashboard/edit_trip.html',
        context
    )


@login_required
def delete_trip(request, trip_id):

    trip = get_object_or_404(
        Trip,
        id=trip_id
    )

    if request.method == 'POST':

        trip.delete()

        return redirect(
            'trips'
        )

    context = {
        'trip': trip,
    }

    return render(
        request,
        'dashboard/delete_trip.html',
        context
    )

@login_required
def expenses(request):

    search = request.GET.get('search', '').strip()

    expense_list = Expense.objects.select_related(
        'vehicle'
    ).all()

    if search:

        expense_list = expense_list.filter(
            Q(vehicle__registration_number__icontains=search) |
            Q(description__icontains=search) |
            Q(notes__icontains=search)
        )

    expense_list = expense_list.order_by(
        '-expense_date'
    )

    context = {
        'expenses': expense_list,
        'search': search,
    }

    return render(
        request,
        'dashboard/expenses.html',
        context
    )


@login_required
def add_expense(request):

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'expenses'
            )

    else:

        form = ExpenseForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_expense.html',
        context
    )


@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            return redirect(
                'expenses'
            )

    else:

        form = ExpenseForm(
            instance=expense
        )

    context = {
        'form': form,
        'expense': expense,
    }

    return render(
        request,
        'dashboard/edit_expense.html',
        context
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == 'POST':

        expense.delete()

        return redirect(
            'expenses'
        )

    context = {
        'expense': expense,
    }

    return render(
        request,
        'dashboard/delete_expense.html',
        context
    )

@login_required
def fuel_efficiency(request):

    vehicles = Vehicle.objects.all()

    efficiency_data = []

    for vehicle in vehicles:

        fuel_records = vehicle.fuel_records.all()

        total_litres = sum(
            record.litres
            for record in fuel_records
        )

        total_cost = sum(
            record.cost
            for record in fuel_records
        )

        mileages = [
            record.mileage
            for record in fuel_records
            if record.mileage is not None
        ]

        if len(mileages) >= 2:

            distance = max(mileages) - min(mileages)

        else:

            distance = 0

        if total_litres > 0 and distance > 0:

            efficiency = distance / total_litres
            cost_per_km = total_cost / distance

        else:

            efficiency = 0
            cost_per_km = 0

        efficiency_data.append({
            'vehicle': vehicle,
            'total_litres': total_litres,
            'total_cost': total_cost,
            'distance': distance,
            'efficiency': efficiency,
            'cost_per_km': cost_per_km,
        })

    context = {
        'efficiency_data': efficiency_data,
    }

    return render(
        request,
        'dashboard/fuel_efficiency.html',
        context
    )

@login_required
def fleet_settings(request):

    settings = FleetSetting.objects.first()

    if settings is None:
        settings = FleetSetting.objects.create()

    if request.method == 'POST':

        form = FleetSettingForm(
            request.POST,
            instance=settings
        )

        if form.is_valid():

            form.save()

            return redirect('fleet_settings')

    else:

        form = FleetSettingForm(
            instance=settings
        )

    context = {
        'form': form,
        'settings': settings,
    }

    return render(
        request,
        'dashboard/fleet_settings.html',
        context
    )

@login_required
def user_management(request):

    users = User.objects.all().order_by('-date_joined')

    context = {
        'users': users,
    }

    return render(
        request,
        'dashboard/user_management.html',
        context
    )

@login_required
def user_management(request):

    users = User.objects.all().order_by('-date_joined')

    context = {
        'users': users,
    }

    return render(
        request,
        'dashboard/user_management.html',
        context
    )


@login_required
def toggle_user_status(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':

        # Prevent the currently logged-in user
        # from accidentally disabling their own account.
        if user.id != request.user.id:

            user.is_active = not user.is_active
            user.save()

    return redirect('user_management')

@login_required
def data_export(request):

    return render(
        request,
        'dashboard/data_export.html'
    )

@login_required
def export_vehicles(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="vehicles.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Registration Number',
        'Vehicle Type',
        'Driver',
        'Status',
        'Speed',
        'Location',
        'Latitude',
        'Longitude',
    ])

    vehicles = Vehicle.objects.all()

    for vehicle in vehicles:

        writer.writerow([
            vehicle.registration_number,
            vehicle.vehicle_type,
            vehicle.driver,
            vehicle.get_status_display(),
            vehicle.speed,
            vehicle.location,
            vehicle.latitude,
            vehicle.longitude,
        ])

    return response

@login_required
def export_drivers(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="drivers.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Name',
        'Phone',
        'License Number',
        'Vehicle',
    ])

    drivers = Driver.objects.select_related(
        'vehicle'
    ).all()

    for driver in drivers:

        writer.writerow([
            driver.name,
            driver.phone,
            driver.license_number,
            driver.vehicle.registration_number
            if driver.vehicle else '',
        ])

    return response

@login_required
def export_fuel(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="fuel_records.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Vehicle',
        'Fuel Date',
        'Litres',
        'Cost',
        'Mileage',
        'Fuel Station',
        'Notes',
    ])

    records = FuelRecord.objects.select_related(
        'vehicle'
    ).all()

    for record in records:

        writer.writerow([
            record.vehicle.registration_number,
            record.fuel_date,
            record.litres,
            record.cost,
            record.mileage,
            record.fuel_station,
            record.notes,
        ])

    return response

@login_required
def export_maintenance(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="maintenance_records.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Vehicle',
        'Maintenance Type',
        'Description',
        'Service Date',
        'Next Service Date',
        'Mileage',
        'Cost',
        'Service Provider',
        'Status',
        'Notes',
    ])

    records = MaintenanceRecord.objects.select_related(
        'vehicle'
    ).all()

    for record in records:

        writer.writerow([
            record.vehicle.registration_number,
            record.get_maintenance_type_display(),
            record.description,
            record.service_date,
            record.next_service_date,
            record.mileage,
            record.cost,
            record.service_provider,
            record.get_status_display(),
            record.notes,
        ])

    return response

@login_required
def export_trips(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="trips.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Vehicle',
        'Driver',
        'Start Location',
        'Destination',
        'Start Time',
        'End Time',
        'Distance',
        'Status',
        'Notes',
    ])

    trips = Trip.objects.select_related(
        'vehicle',
        'driver'
    ).all()

    for trip in trips:

        writer.writerow([
            trip.vehicle.registration_number,
            trip.driver.name if trip.driver else '',
            trip.start_location,
            trip.destination,
            trip.start_time,
            trip.end_time,
            trip.distance,
            trip.get_status_display(),
            trip.notes,
        ])

    return response

@login_required
def export_expenses(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="expenses.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Vehicle',
        'Expense Type',
        'Expense Date',
        'Amount',
        'Description',
        'Notes',
    ])

    expenses = Expense.objects.select_related(
        'vehicle'
    ).all()

    for expense in expenses:

        writer.writerow([
            expense.vehicle.registration_number,
            expense.get_expense_type_display(),
            expense.expense_date,
            expense.amount,
            expense.description,
            expense.notes,
        ])

    return response

@login_required
def crm_activities(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    activity_list = CRMActivity.objects.all()

    if search:
        activity_list = activity_list.filter(
            Q(client_name__icontains=search) |
            Q(description__icontains=search) |
            Q(notes__icontains=search)
        )

    if status:
        activity_list = activity_list.filter(status=status)

    activity_list = activity_list.order_by(
        '-activity_date',
        '-created_at'
    )

    context = {
        'crm_activities': activity_list,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'dashboard/crm_activities.html',
        context
    )


@login_required
def add_crm_activity(request):
    if request.method == 'POST':
        form = CRMActivityForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('crm_activities')
    else:
        form = CRMActivityForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_crm_activity.html',
        context
    )

@login_required
def support_tickets(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()

    ticket_list = SupportTicket.objects.select_related(
        'vehicle'
    ).all()

    if search:
        ticket_list = ticket_list.filter(
            Q(issue__icontains=search) |
            Q(description__icontains=search) |
            Q(notes__icontains=search) |
            Q(vehicle__registration_number__icontains=search)
        )

    if status:
        ticket_list = ticket_list.filter(status=status)

    if priority:
        ticket_list = ticket_list.filter(priority=priority)

    ticket_list = ticket_list.order_by('-created_at')

    context = {
        'support_tickets': ticket_list,
        'search': search,
        'selected_status': status,
        'selected_priority': priority,
    }

    return render(
        request,
        'dashboard/support_tickets.html',
        context
    )


@login_required
def add_support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('support_tickets')
    else:
        form = SupportTicketForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'dashboard/add_support_ticket.html',
        context
    )


@login_required
def resolve_support_ticket(request, ticket_id):
    ticket = get_object_or_404(
        SupportTicket,
        id=ticket_id
    )

    if request.method == 'POST':
        ticket.status = 'resolved'
        ticket.save()

    return redirect('support_tickets')
