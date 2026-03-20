from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from booking.models import Booking


class PaymentConfirmAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = Booking.objects.filter(id=booking_id, customer=request.user.customer).first()
        if not booking:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        booking.status = 'confirmed'
        booking.admin_status = 'approved'
        booking.save()

        return Response({
            'detail': 'Payment success (sandbox).',
            'payment_id': f'PAY-{booking.id}'
        })


class PaymentRefundAPIView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = Booking.objects.filter(id=booking_id, customer=request.user.customer).first()
        if not booking:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        booking.status = 'cancelled'
        booking.admin_status = 'rejected'
        booking.save()

        return Response({
            'detail': 'Refund success (sandbox).',
            'refund_id': f'REF-{booking.id}'
        })