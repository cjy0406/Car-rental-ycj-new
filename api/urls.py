from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PaymentConfirmAPIView, PaymentRefundAPIView

urlpatterns = [
    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Payment APIs
    path('payments/confirm/', PaymentConfirmAPIView.as_view(), name='payment_confirm'),
    path('payments/refund/', PaymentRefundAPIView.as_view(), name='payment_refund'),
]