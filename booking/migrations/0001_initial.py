from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('admin_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('return_confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('return_notes', models.TextField(blank=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='vendors.car')),\n                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='customers.customer')),\n            ],\n        ),\n        migrations.CreateModel(\n            name='ReturnRecord',\n            fields=[\n                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),\n                ('is_active', models.BooleanField(default=True)),\n                ('created_at', models.DateTimeField(auto_now_add=True)),\n                ('updated_at', models.DateTimeField(auto_now=True)),\n                ('confirmed_at', models.DateTimeField(auto_now_add=True)),\n                ('condition_notes', models.TextField(blank=True)),\n                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='return_record', to='booking.booking')),\n                ('confirmed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),\n            ],\n        ),\n        migrations.CreateModel(\n            name='Review',\n            fields=[\n                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),\n                ('is_active', models.BooleanField(default=True)),\n                ('created_at', models.DateTimeField(auto_now_add=True)),\n                ('updated_at', models.DateTimeField(auto_now=True)),\n                ('rating', models.PositiveSmallIntegerField(default=5)),\n                ('comment', models.TextField(blank=True)),\n                ('reply', models.TextField(blank=True)),\n                ('replied_at', models.DateTimeField(blank=True, null=True)),\n                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='booking.booking')),\n                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='vendors.car')),\n                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='customers.customer')),\n                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='vendors.vendor')),\n            ],\n        ),\n    ]