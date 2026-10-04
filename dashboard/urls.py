from django.urls import path

from .views import (
    dashboard_home,
    vehicles,
    add_vehicle,
    vehicle_detail,
    edit_vehicle,
    delete_vehicle,
    live_tracking,
    update_vehicle_location,
    vehicle_locations_api,
    vehicle_history,
    fleet_analytics,
    maintenance_records,
    add_maintenance,
    fuel_records,
    add_fuel,
    drivers,
    add_driver,
    edit_driver,
    delete_driver,
    alerts,
    add_alert,
    mark_alert_read,
    delete_alert,
    vehicle_documents,
    add_vehicle_document,
    delete_vehicle_document,
    add_trip,
    trips,
    edit_trip,
    delete_trip,
    expenses,
    add_expense,
    edit_expense,
    delete_expense,
    fuel_efficiency,
    reports,
    fleet_settings,
    user_management,
    toggle_user_status,
    data_export,
    export_vehicles,
    export_drivers,
    export_fuel,
    export_maintenance,
    export_trips,
    export_expenses,
    crm_activities,
    add_crm_activity,
    support_tickets,
    add_support_ticket,
    resolve_support_ticket,
)


urlpatterns = [

    path(
        '',
        dashboard_home,
        name='dashboard'
    ),

    path(
        'vehicles/',
        vehicles,
        name='vehicles'
    ),

    path(
        'vehicles/add/',
        add_vehicle,
        name='add_vehicle'
    ),

    path(
        'vehicles/<int:vehicle_id>/',
        vehicle_detail,
        name='vehicle_detail'
    ),

    path(
        'vehicles/<int:vehicle_id>/edit/',
        edit_vehicle,
        name='edit_vehicle'
    ),

    path(
        'vehicles/<int:vehicle_id>/delete/',
        delete_vehicle,
        name='delete_vehicle'
    ),

    path(
        'live-tracking/',
        live_tracking,
        name='live_tracking'
    ),

    path(
        'vehicles/<int:vehicle_id>/update-location/',
        update_vehicle_location,
        name='update_vehicle_location'
    ),

    path(
        'api/vehicle-locations/',
        vehicle_locations_api,
        name='vehicle_locations_api'
    ),

path(
    'vehicles/<int:vehicle_id>/history/',
    vehicle_history,
    name='vehicle_history'
),

path(
    'analytics/',
    fleet_analytics,
    name='fleet_analytics'
),

    path(
        'maintenance/',
        maintenance_records,
        name='maintenance_records'
    ),

    path(
        'maintenance/add/',
        add_maintenance,
        name='add_maintenance'
    ),

    path(
        'fuel/',
         fuel_records,
         name='fuel_records'
    ),

    path(
        'fuel/add/',
         add_fuel,
         name='add_fuel'
         ),

    path('drivers/', drivers, name='drivers'),
    path('drivers/add/', add_driver, name='add_driver'),
    path('drivers/<int:driver_id>/edit/', edit_driver, name='edit_driver'),

    path(
    'drivers/<int:driver_id>/delete/',
    delete_driver,
    name='delete_driver'
),

path('alerts/', alerts, name='alerts'),
path('alerts/add/', add_alert, name='add_alert'),

path(
    'alerts/<int:alert_id>/read/',
    mark_alert_read,
    name='mark_alert_read'
),

path(
    'alerts/<int:alert_id>/delete/',
    delete_alert,
    name='delete_alert'
),

path(
    'vehicle-documents/',
    vehicle_documents,
    name='vehicle_documents'
),

path(
    'vehicle-documents/add/',
    add_vehicle_document,
    name='add_vehicle_document'
),

path(
    'vehicle-documents/<int:document_id>/delete/',
    delete_vehicle_document,
    name='delete_vehicle_document'
),

path('trips/', trips, name='trips'),
path('trips/add/', add_trip, name='add_trip'),

path(
    'trips/<int:trip_id>/edit/',
    edit_trip,
    name='edit_trip'
),

path(
    'trips/<int:trip_id>/delete/',
    delete_trip,
    name='delete_trip'
),

path(
    'expenses/',
    expenses,
    name='expenses'
),

path(
    'expenses/add/',
    add_expense,
    name='add_expense'
),

path(
    'expenses/<int:expense_id>/edit/',
    edit_expense,
    name='edit_expense'
),

path(
    'expenses/<int:expense_id>/delete/',
    delete_expense,
    name='delete_expense'
),

path(
    'fuel-efficiency/',
    fuel_efficiency,
    name='fuel_efficiency'
),

path('reports/', reports, name='reports'),

path(
    'settings/',
    fleet_settings,
    name='fleet_settings'
),

path(
    'users/',
    user_management,
    name='user_management'
),

path(
    'users/<int:user_id>/toggle-status/',
    toggle_user_status,
    name='toggle_user_status'
),

    path('crm/', crm_activities, name='crm_activities'),
    path('crm/add/', add_crm_activity, name='add_crm_activity'),

    path('support/', support_tickets, name='support_tickets'),
    path('support/add/', add_support_ticket, name='add_support_ticket'),
    path(
        'support/<int:ticket_id>/resolve/',
        resolve_support_ticket,
        name='resolve_support_ticket'
    ),

path(
    'export/',
    data_export,
    name='data_export'
),

path(
    'export/vehicles/',
    export_vehicles,
    name='export_vehicles'
),

path(
    'export/drivers/',
    export_drivers,
    name='export_drivers'
),

path(
    'export/fuel/',
    export_fuel,
    name='export_fuel'
),

path(
    'export/maintenance/',
    export_maintenance,
    name='export_maintenance'
),

path(
    'export/trips/',
    export_trips,
    name='export_trips'
),

path(
    'export/expenses/',
    export_expenses,
    name='export_expenses'
),



]