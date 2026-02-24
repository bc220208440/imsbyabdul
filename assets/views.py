from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from collections import defaultdict
import json

from .models import CustomUser, Asset, Category, Location
from .forms import (CustomUserCreationForm, CustomUserChangeForm, AssetForm, 
                    AssetUpdateStatusForm, CategoryForm, LocationForm, AssetSearchForm)


# ============================================================================
# ROLE-BASED ACCESS MIXINS
# ============================================================================

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to check if user is Admin"""
    def test_func(self):
        return self.request.user.role == 'ADMIN'
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('asset_list')


class AdminOrManagerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to check if user is Admin or Manager"""
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'MANAGER']
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('asset_list')


class LoginRequiredView(LoginRequiredMixin):
    """Basic login required mixin for all views"""
    pass


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('asset_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('asset_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ============================================================================
# ASSET VIEWS - CRUD OPERATIONS
# ============================================================================

class AssetListView(LoginRequiredView, ListView):
    """List all assets with search and filtering"""
    model = Asset
    template_name = 'assets/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 20

    def get_queryset(self):
        queryset = Asset.objects.select_related('category', 'location', 'created_by').all()
        
        # Search functionality
        search_form = AssetSearchForm(self.request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            search_type = search_form.cleaned_data.get('search_type')
            
            if search_query:
                if search_type == 'name':
                    queryset = queryset.filter(name__icontains=search_query)
                elif search_type == 'serial':
                    queryset = queryset.filter(serial_number__icontains=search_query)
                else:
                    queryset = queryset.filter(
                        Q(name__icontains=search_query) |
                        Q(serial_number__icontains=search_query)
                    )
            
            # Category filter
            category_id = search_form.cleaned_data.get('category')
            if category_id:
                queryset = queryset.filter(category=category_id)
            
            # Location filter
            location_id = search_form.cleaned_data.get('location')
            if location_id:
                queryset = queryset.filter(location=location_id)
            
            # Status filter
            status = search_form.cleaned_data.get('status')
            if status:
                queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = AssetSearchForm(self.request.GET)
        context['total_assets'] = Asset.objects.count()
        context['available_assets'] = Asset.objects.filter(status='AVAILABLE').count()
        context['in_use_assets'] = Asset.objects.filter(status='IN_USE').count()
        context['user_role'] = self.request.user.role
        return context


class AssetDetailView(LoginRequiredView, DetailView):
    """View asset details"""
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        context['can_edit'] = self.request.user.role in ['ADMIN', 'MANAGER']
        context['can_delete'] = self.request.user.role == 'ADMIN'
        return context


class AssetCreateView(AdminRequiredMixin, CreateView):
    """Create new asset (Admin only)"""
    model = Asset
    form_class = AssetForm
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('asset_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Asset created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        context['title'] = 'Add New Asset'
        context['user_role'] = self.request.user.role
        return context


class AssetUpdateView(AdminOrManagerMixin, UpdateView):
    """Update asset"""
    model = Asset
    template_name = 'assets/asset_form.html'
    success_url = reverse_lazy('asset_list')

    def test_func(self):
        if not super().test_func():
            return False
        # Managers can only update status/location
        if self.request.user.role == 'MANAGER':
            return True
        return True

    def get_form_class(self):
        # Managers can only update status and location
        if self.request.user.role == 'MANAGER':
            return AssetUpdateStatusForm
        # Admins can update everything
        return AssetForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Asset updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        context['title'] = f'Edit {self.object.name}'
        context['user_role'] = self.request.user.role
        return context


class AssetDeleteView(AdminRequiredMixin, DeleteView):
    """Delete asset (Admin only)"""
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = reverse_lazy('asset_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Asset deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# CATEGORY VIEWS - CRUD OPERATIONS
# ============================================================================

class CategoryListView(LoginRequiredView, ListView):
    """List all categories"""
    model = Category
    template_name = 'assets/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        # Count assets per category
        for category in context['categories']:
            category.asset_count = category.assets.count()
            category.available_count = category.assets.filter(status='AVAILABLE').count()
        return context


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """Create new category (Admin only)"""
    model = Category
    form_class = CategoryForm
    template_name = 'assets/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        context['title'] = 'Add New Category'
        return context


class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """Update category (Admin only)"""
    model = Category
    form_class = CategoryForm
    template_name = 'assets/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        context['title'] = f'Edit {self.object.name}'
        return context


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """Delete category (Admin only)"""
    model = Category
    template_name = 'assets/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except:
            messages.error(request, 'Cannot delete category with associated assets.')
            return redirect('category_list')


# ============================================================================
# LOCATION VIEWS - CRUD OPERATIONS
# ============================================================================

class LocationListView(LoginRequiredView, ListView):
    """List all locations"""
    model = Location
    template_name = 'assets/location_list.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        # Count assets per location
        for location in context['locations']:
            location.asset_count = location.assets.count()
        return context


class LocationCreateView(AdminRequiredMixin, CreateView):
    """Create new location (Admin only)"""
    model = Location
    form_class = LocationForm
    template_name = 'assets/location_form.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        messages.success(self.request, 'Location created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        context['title'] = 'Add New Location'
        return context


class LocationUpdateView(AdminRequiredMixin, UpdateView):
    """Update location (Admin only)"""
    model = Location
    form_class = LocationForm
    template_name = 'assets/location_form.html'
    success_url = reverse_lazy('location_list')

    def form_valid(self, form):
        messages.success(self.request, 'Location updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        context['title'] = f'Edit {self.object.name}'
        return context


class LocationDeleteView(AdminRequiredMixin, DeleteView):
    """Delete location (Admin only)"""
    model = Location
    template_name = 'assets/location_confirm_delete.html'
    success_url = reverse_lazy('location_list')

    def delete(self, request, *args, **kwargs):
        # Set assets to null if location has assets
        self.object.assets.all().update(location=None)
        messages.success(request, 'Location deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# USER MANAGEMENT VIEWS
# ============================================================================

class UserListView(AdminRequiredMixin, ListView):
    """List all users (Admin only)"""
    model = CustomUser
    template_name = 'assets/user_list.html'
    context_object_name = 'users'
    paginate_by = 20


class UserCreateView(AdminRequiredMixin, CreateView):
    """Create new user (Admin only)"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'assets/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        context['title'] = 'Add New User'
        return context


class UserUpdateView(AdminRequiredMixin, UpdateView):
    """Update user (Admin only)"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'assets/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        context['title'] = f'Edit {self.object.username}'
        return context


class UserDeleteView(AdminRequiredMixin, DeleteView):
    """Delete user (Admin only)"""
    model = CustomUser
    template_name = 'assets/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# DASHBOARD AND REPORT VIEWS
# ============================================================================

class DashboardView(LoginRequiredView, View):
    """Dashboard with summary statistics"""
    template_name = 'assets/dashboard.html'

    def get(self, request):
        from django.db.models import Sum
        
        context = {
            'total_assets': Asset.objects.count(),
            'available_assets': Asset.objects.filter(status='AVAILABLE').count(),
            'in_use_assets': Asset.objects.filter(status='IN_USE').count(),
            'in_repair_assets': Asset.objects.filter(status='IN_REPAIR').count(),
            'in_stock_assets': Asset.objects.filter(status='IN_STOCK').count(),
            'total_categories': Category.objects.count(),
            'total_locations': Location.objects.count(),
            'total_users': CustomUser.objects.count(),
            'user_role': request.user.role,
        }

        # Add low stock categories
        low_stock_categories = []
        for category in Category.objects.all():
            available_quantity = category.assets.filter(status='AVAILABLE').aggregate(
                total=Sum('quantity')
            )['total'] or 0
            if available_quantity < category.low_stock_threshold:
                low_stock_categories.append({
                    'category': category,
                    'available': available_quantity,
                    'threshold': category.low_stock_threshold
                })
        context['low_stock_categories'] = low_stock_categories

        return render(request, self.template_name, context)


class AssetsByLocationReportView(LoginRequiredView, View):
    """Report: Assets by Location"""
    template_name = 'assets/report_assets_by_location.html'

    def get(self, request):
        location_id = request.GET.get('location')
        locations = Location.objects.annotate(asset_count=Count('assets'))
        
        data = []
        if location_id:
            location = get_object_or_404(Location, pk=location_id)
            assets = Asset.objects.filter(location=location).select_related('category')
            data = assets
        
        context = {
            'locations': locations,
            'selected_location': location_id,
            'assets': data,
            'user_role': request.user.role,
        }
        return render(request, self.template_name, context)


class LowStockReportView(LoginRequiredView, View):
    """Report: Low Stock items"""
    template_name = 'assets/report_low_stock.html'

    def get(self, request):
        from django.db.models import Sum
        low_stock_data = []
        
        for category in Category.objects.all():
            available_quantity = category.assets.filter(status='AVAILABLE').aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            if available_quantity < category.low_stock_threshold:
                low_stock_data.append({
                    'category': category,
                    'available': available_quantity,
                    'threshold': category.low_stock_threshold,
                    'deficit': category.low_stock_threshold - available_quantity,
                    'assets': category.assets.filter(status='AVAILABLE')
                })
        
        context = {
            'low_stock_items': low_stock_data,
            'user_role': request.user.role,
        }
        return render(request, self.template_name, context)
