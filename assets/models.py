from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('VIEWER', 'Viewer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='VIEWER')

    def __str__(self):
        return f"{self.username} - {self.role}"


class Category(models.Model):
    """Asset categories like IT Equipment, Office Furniture, Tools"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    low_stock_threshold = models.IntegerField(default=5, help_text="Low stock alert threshold")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Location(models.Model):
    """Predefined locations for assets"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Asset(models.Model):
    """Asset model for inventory tracking"""
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('IN_USE', 'In Use'),
        ('IN_REPAIR', 'In Repair'),
        ('IN_STOCK', 'In Stock'),
    )

    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='assets')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='assets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    quantity = models.IntegerField(default=1, help_text="Total number of this asset in inventory")
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                                   limit_choices_to={'role': 'MANAGER'}, related_name='assigned_assets')
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, 
                                  related_name='created_assets', editable=False)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='updated_assets', editable=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['category']),
            models.Index(fields=['location']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.name} ({self.serial_number})"