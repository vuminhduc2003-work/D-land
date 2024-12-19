from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'residents', views.ResidentViewSet)
router.register(r'family-members', views.FamilyMemberViewSet)
router.register(r'apartments', views.ApartmentViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'facilities', views.FacilityViewSet)
router.register(r'service-fees', views.ServiceFeeViewSet)
router.register(r'maintenance-requests', views.MaintenanceRequestViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'entry-exit-history', views.EntryExitHistoryViewSet)
router.register(r'rental-agreements', views.RentalAgreementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # All routes will be prefixed with 'api/'
]
