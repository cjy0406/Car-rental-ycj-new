from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CarList, CarDetail,
    BookingCreate, BookingList,
    ReturnConfirm,
    ReviewCreate, ReviewList, ReviewReply,
    VendorWithdrawal,
    AdminBookingApproval, AdminCarApproval, AdminWithdrawal,
    AnalyticsSummary,
    PaymentConfirmAPIView, PaymentRefundAPIView,
)

urlpatterns = [
    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cars
    path('cars/', CarList.as_view(), name='car_list'),
    path('cars/<uuid:car_id>/', CarDetail.as_view(), name='car_detail'),

    # Bookings
    path('bookings/', BookingList.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreate.as_view(), name='booking_create'),
    path('bookings/<uuid:booking_id>/return/', ReturnConfirm.as_view(), name='return_confirm'),

    # Reviews
    path('reviews/', ReviewList.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreate.as_view(), name='review_create'),
    path('reviews/<uuid:review_id>/reply/', ReviewReply.as_view(), name='review_reply'),

    # Vendor withdrawal
    path('withdrawals/', VendorWithdrawal.as_view(), name='vendor_withdrawal'),

    # Admin actions
    path('admin/bookings/<uuid:booking_id>/approval/', AdminBookingApproval.as_view(), name='admin_booking_approval'),
    path('admin/cars/<uuid:car_id>/approval/', AdminCarApproval.as_view(), name='admin_car_approval'),
    path('admin/withdrawals/<uuid:withdrawal_id>/', AdminWithdrawal.as_view(), name='admin_withdrawal'),

    # Analytics
    path('analytics/summary/', AnalyticsSummary.as_view(), name='analytics_summary'),

    # Payments
    path('payments/confirm/', PaymentConfirmAPIView.as_view(), name='payment_confirm'),
    path('payments/refund/', PaymentRefundAPIView.as_view(), name='payment_refund'),
]