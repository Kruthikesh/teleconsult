# from apps.user.views import DashboardView
from django.urls import path
from apps.patient.views import AuthViewSet
# urlpatterns = [
#     path('api/register/', RegisterAPI.as_view(), name='register'),
# ]

# router = routers.DefaultRouter(trailing_slash=False)
# router.register('api/auth', AuthViewSet, basename='auth')