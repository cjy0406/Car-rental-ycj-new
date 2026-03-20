from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from django.utils import timezone

from vendors.models import Car, WithdrawalRequest
from booking.models import Booking, ReturnRecord, Review
from .serializers import CarSerializer, BookingSerializer, ReturnRecordSerializer, ReviewSerializer, WithdrawalRequestSerializer


class CarList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cars = Car.objects.filter(is_available=True, is_approved=True)
        car_type = request.GET.get('type')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        search = request.GET.get('search')

        if car_type:
            cars = cars.filter(car_type=car_type)
        if min_price:
            cars = cars.filter(price_per_day__gte=min_price)
        if max_price:
            cars = cars.filter(price_per_day__lte=max_price)
        if search:
            cars = cars.filter(Q(name__icontains=search) | Q(description__icontains=search))

        return Response({'cars': CarSerializer(cars, many=True).data}, status=status.HTTP_200_OK)


class CarDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, car_id):
        car = Car.objects.filter(id=car_id, is_approved=True).first()
        if not car:
            return Response({'detail': 'Car not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'car': CarSerializer(car).data}, status=status.HTTP_200_OK)


class BookingCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = getattr(request.user, 'customer', None)
        if not customer:
            return Response({'detail': 'Only customers can book cars.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        car = Car.objects.filter(id=serializer.validated_data['car'].id, is_approved=True, is_available=True).first()
        if not car:
            return Response({'detail': 'Car not available.'}, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        days = (end_date - start_date).days
        total_price = days * car.price_per_day

        booking = Booking.objects.create(
            car=car,
            customer=customer,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='pending',
            admin_status='pending',
        )
        return Response({'booking': BookingSerializer(booking).data}, status=status.HTTP_201_CREATED)


class BookingList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = getattr(request.user, 'customer', None)
        if not customer:
            return Response({'detail': 'Only customers can view bookings.'}, status=status.HTTP_403_FORBIDDEN)
        bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
        return Response({'bookings': BookingSerializer(bookings, many=True).data}, status=status.HTTP_200_OK)


class ReturnConfirm(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        customer = getattr(request.user, 'customer', None)
        if not customer:
            return Response({'detail': 'Only customers can confirm return.'}, status=status.HTTP_403_FORBIDDEN)

        booking = Booking.objects.filter(id=booking_id, customer=customer).first()
        if not booking:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        if booking.status not in ['confirmed', 'completed']:
            return Response({'detail': 'Booking is not eligible for return.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'completed'
        booking.return_confirmed_at = timezone.now()
        booking.return_notes = request.data.get('return_notes', '')
        booking.save()

        return_record, _ = ReturnRecord.objects.get_or_create(
            booking=booking,
            defaults={
                'confirmed_by': request.user,
                'condition_notes': request.data.get('condition_notes', '')
            }
        )

        return Response({'return_record': ReturnRecordSerializer(return_record).data}, status=status.HTTP_200_OK)


class ReviewCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = getattr(request.user, 'customer', None)
        if not customer:
            return Response({'detail': 'Only customers can review.'}, status=status.HTTP_403_FORBIDDEN)

        booking_id = request.data.get('booking')
        booking = Booking.objects.filter(id=booking_id, customer=customer, status='completed').first()
        if not booking:
            return Response({'detail': 'Completed booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(booking, 'review'):
            return Response({'detail': 'Review already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            booking=booking,
            customer=customer,
            vendor=booking.car.vendor,
            car=booking.car,
            rating=serializer.validated_data.get('rating', 5),
            comment=serializer.validated_data.get('comment', '')
        )

        return Response({'review': ReviewSerializer(review).data}, status=status.HTTP_201_CREATED)


class ReviewList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendor = getattr(request.user, 'vendor', None)
        customer = getattr(request.user, 'customer', None)
        if vendor:
            reviews = Review.objects.filter(vendor=vendor).order_by('-created_at')
        elif customer:
            reviews = Review.objects.filter(customer=customer).order_by('-created_at')
        else:
            reviews = Review.objects.all().order_by('-created_at')
        return Response({'reviews': ReviewSerializer(reviews, many=True).data}, status=status.HTTP_200_OK)


class ReviewReply(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        vendor = getattr(request.user, 'vendor', None)
        if not vendor:
            return Response({'detail': 'Only vendors can reply.'}, status=status.HTTP_403_FORBIDDEN)

        review = Review.objects.filter(id=review_id, vendor=vendor).first()
        if not review:
            return Response({'detail': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

        review.reply = request.data.get('reply', '')
        review.replied_at = timezone.now()
        review.save()
        return Response({'review': ReviewSerializer(review).data}, status=status.HTTP_200_OK)


class VendorWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vendor = getattr(request.user, 'vendor', None)
        if not vendor:
            return Response({'detail': 'Only vendors can withdraw.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = WithdrawalRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        withdrawal = WithdrawalRequest.objects.create(
            vendor=vendor,
            amount=serializer.validated_data['amount'],
            status='pending'
        )
        return Response({'withdrawal': WithdrawalRequestSerializer(withdrawal).data}, status=status.HTTP_201_CREATED)


class AdminBookingApproval(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        if not request.user.is_staff:
            return Response({'detail': 'Admin only.'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action', 'approve')
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'approve':
            booking.admin_status = 'approved'
            if booking.status == 'pending':
                booking.status = 'confirmed'
        else:
            booking.admin_status = 'rejected'
            booking.status = 'cancelled'
        booking.save()
        return Response({'booking': BookingSerializer(booking).data}, status=status.HTTP_200_OK)


class AdminCarApproval(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, car_id):
        if not request.user.is_staff:
            return Response({'detail': 'Admin only.'}, status=status.HTTP_403_FORBIDDEN)
        car = Car.objects.filter(id=car_id).first()
        if not car:
            return Response({'detail': 'Car not found.'}, status=status.HTTP_404_NOT_FOUND)
        car.is_approved = True
        car.save()
        return Response({'car': CarSerializer(car).data}, status=status.HTTP_200_OK)


class AdminWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, withdrawal_id):
        if not request.user.is_staff:
            return Response({'detail': 'Admin only.'}, status=status.HTTP_403_FORBIDDEN)

        withdrawal = WithdrawalRequest.objects.filter(id=withdrawal_id).first()
        if not withdrawal:
            return Response({'detail': 'Withdrawal not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action', 'approve')
        if action == 'approve':
            withdrawal.status = 'approved'
        elif action == 'paid':
            withdrawal.status = 'paid'
        else:
            withdrawal.status = 'rejected'
        withdrawal.processed_at = timezone.now()
        withdrawal.notes = request.data.get('notes', '')
        withdrawal.save()
        return Response({'withdrawal': WithdrawalRequestSerializer(withdrawal).data}, status=status.HTTP_200_OK)


class AnalyticsSummary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({'detail': 'Admin only.'}, status=status.HTTP_403_FORBIDDEN)

        total_cars = Car.objects.count()
        total_bookings = Booking.objects.count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        revenue = Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(total=Sum('total_price'))['total'] or 0

        return Response({
            'summary': {
                'total_cars': total_cars,
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'revenue': revenue,
            }
        }, status=status.HTTP_200_OK)


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
