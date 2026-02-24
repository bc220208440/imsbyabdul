from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Asset, Category, Location
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin for CustomUser model"""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role', {'fields': ('role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    list_display = ('name', 'low_stock_threshold', 'asset_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description', 'low_stock_threshold')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def asset_count(self, obj):
        """Display count of assets in this category"""
        return obj.assets.count()
    asset_count.short_description = 'Assets'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin for Location model"""
    list_display = ('name', 'asset_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def asset_count(self, obj):
        """Display count of assets at this location"""
        return obj.assets.count()
    asset_count.short_description = 'Assets'


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin for Asset model"""
    list_display = ('name', 'serial_number', 'category', 'location', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'category', 'location', 'created_at', 'purchase_date')
    search_fields = ('name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Asset Information', {
            'fields': ('name', 'serial_number', 'category', 'location', 'status')
        }),
        ('Purchase Details', {
            'fields': ('purchase_date', 'purchase_price'),
            'classes': ('collapse',)
        }),
        ('Assignment', {
            'fields': ('assigned_to',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Automatically tracked system information'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by on save"""
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Filter querysets based on user role"""
        queryset = super().get_queryset(request)
        # Allow admins to see all, everyone else can see as well (can customize if needed)
        return queryset
