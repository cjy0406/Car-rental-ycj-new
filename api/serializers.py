from rest_framework import serializers
from django.contrib.auth import get_user_model
from vendors.models import Vendor, Car, CarImage, WithdrawalRequest
from customers.models import Customer
from booking.models import Booking, ReturnRecord, Review
from datetime import datetime

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class VendorRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Vendor
        fields = ['username', 'password', 'email', 'name', 'contact_email', 'phone', 'address']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        vendor = Vendor.objects.create(user=user, is_approved=False, **validated_data)
        return vendor


class CustomerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'phone', 'address']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'image', 'order']


class CarSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            'id', 'name', 'description', 'image', 'images',
            'car_type', 'model_year', 'price_per_day',
            'is_available', 'is_approved', 'vendor', 'vendor_name',
            'created_at'
        ]
        read_only_fields = ['vendor', 'is_approved', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(source='car.name', read_only=True)
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'car', 'car_name',
            'customer', 'customer_name',
            'start_date', 'end_date', 'total_price',
            'status', 'admin_status', 'return_confirmed_at', 'return_notes', 'created_at'
        ]
        read_only_fields = ['customer', 'total_price', 'status', 'admin_status', 'return_confirmed_at', 'return_notes', 'created_at']

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")
        return attrs


class ReturnRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRecord
        fields = ['id', 'booking', 'confirmed_by', 'confirmed_at', 'condition_notes', 'created_at']
        read_only_fields = ['confirmed_by', 'confirmed_at', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'customer', 'vendor', 'car', 'rating', 'comment', 'reply', 'replied_at', 'created_at']
        read_only_fields = ['customer', 'vendor', 'car', 'reply', 'replied_at', 'created_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['id', 'vendor', 'amount', 'status', 'requested_at', 'processed_at', 'notes']
        read_only_fields = ['vendor', 'status', 'requested_at', 'processed_at']
