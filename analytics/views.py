from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum

from booking.models import Booking
from vendors.models import Vendor

@api_view(['GET'])
@permission_classes([IsAdminUser])
def analytics_summary(request):
    total_vendors = Vendor.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(total=Sum('total_price'))['total'] or 0

    recent_bookings = Booking.objects.select_related('car', 'customer').order_by('-created_at')[:10]
    recent_data = [
        {
            'id': str(b.id),
            'car': b.car.name,
            'customer': b.customer.user.username,
            'total_price': float(b.total_price),
            'status': b.status,
            'created_at': b.created_at,
        }
        for b in recent_bookings
    ]

    return Response({
        'totals': {
            'total_vendors': total_vendors,
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue),
        },
        'recent_bookings': recent_data,
    })