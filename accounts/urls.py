from django.urls import path
from . import views

urlpatterns = [
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),

    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'task/<int:task_id>/toggle/',
        views.toggle_task,
        name='toggle_task'
    ),

    path(
        'task/<int:task_id>/delete/',
        views.delete_task,
        name='delete_task'
    ),

    # Password reset
    path(
        'password-reset/',
        views.FleetPasswordResetView.as_view(),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        views.FleetPasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'password-reset/<uidb64>/<token>/',
        views.FleetPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'password-reset/complete/',
        views.FleetPasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]