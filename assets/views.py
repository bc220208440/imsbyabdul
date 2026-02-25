from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import HttpRequest, HttpResponse
import csv

from .models import CustomUser, Asset, Category, Location
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    AssetForm,
    AssetUpdateStatusForm,
    CategoryForm,
    LocationForm,
    AssetSearchForm,
)

# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# ============================================================
# ASSET VIEWS
# ============================================================

class AssetListView(LoginRequiredMixin, ListView):

    model = Asset
    template_name = "assets/asset_list.html"
    context_object_name = "assets"
    paginate_by = 20

    def get_queryset(self):
        queryset = Asset.objects.select_related(
            "category", "location", "created_by"
        )

        search_form = AssetSearchForm(self.request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get("search")
            search_type = search_form.cleaned_data.get("search_type")

            if search_query:
                if search_type == "name":
                    queryset = queryset.filter(name__icontains=search_query)
                elif search_type == "serial":
                    queryset = queryset.filter(serial_number__icontains=search_query)
                else:
                    queryset = queryset.filter(
                        Q(name__icontains=search_query)
                        | Q(serial_number__icontains=search_query)
                        | Q(category__name__icontains=search_query)
                    )

            if search_form.cleaned_data.get("category"):
                queryset = queryset.filter(
                    category=search_form.cleaned_data["category"]
                )

            if search_form.cleaned_data.get("location"):
                queryset = queryset.filter(
                    location=search_form.cleaned_data["location"]
                )

            if search_form.cleaned_data.get("status"):
                queryset = queryset.filter(
                    status=search_form.cleaned_data["status"]
                )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = AssetSearchForm(self.request.GET)
        context["user_role"] = self.request.user.role if hasattr(self.request.user, "role") else "VIEWER"
        context["total_assets"] = Asset.objects.count()
        return context


class AssetDetailView(LoginRequiredMixin, DetailView):

    model = Asset
    template_name = "assets/asset_detail.html"
    context_object_name = "asset"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = getattr(user, "role", "VIEWER")

        can_edit = user.is_authenticated and role in ("ADMIN", "MANAGER") and user.has_perm(
            "assets.change_asset"
        )
        can_delete = user.is_authenticated and role == "ADMIN" and user.has_perm(
            "assets.delete_asset"
        )

        context["can_edit"] = can_edit
        context["can_delete"] = can_delete
        return context


class AssetCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assets.add_asset"
    raise_exception = True

    model = Asset
    form_class = AssetForm
    template_name = "assets/asset_form.html"
    success_url = reverse_lazy("asset_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Asset created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Create"
        context["title"] = "Create Asset"
        context["user_role"] = getattr(self.request.user, "role", "VIEWER")
        context["status_only"] = False
        return context


class AssetUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assets.change_asset"
    raise_exception = True

    model = Asset
    template_name = "assets/asset_form.html"
    success_url = reverse_lazy("asset_list")

    def get_form_class(self):
        # Managers only have change permission (no delete)
        if not self.request.user.has_perm("assets.delete_asset"):
            return AssetUpdateStatusForm
        return AssetForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Asset updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_status_only = not self.request.user.has_perm("assets.delete_asset")
        context["action"] = "Update Status" if is_status_only else "Update"
        context["title"] = "Update Asset"
        context["user_role"] = getattr(self.request.user, "role", "VIEWER")
        context["status_only"] = is_status_only
        return context


class AssetDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assets.delete_asset"
    raise_exception = True

    model = Asset
    template_name = "assets/asset_confirm_delete.html"
    success_url = reverse_lazy("asset_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Asset deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ============================================================
# CATEGORY VIEWS
# ============================================================

class CategoryListView(LoginRequiredMixin, ListView):

    model = Category
    template_name = "assets/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(
            asset_count=Count("assets"),
            available_count=Sum("assets__quantity", filter=Q(assets__status="AVAILABLE")),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_role"] = self.request.user.role if hasattr(self.request.user, "role") else "VIEWER"
        return context


class CategoryCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assets.add_category"
    raise_exception = True

    model = Category
    form_class = CategoryForm
    template_name = "assets/category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assets.change_category"
    raise_exception = True

    model = Category
    form_class = CategoryForm
    template_name = "assets/category_form.html"
    success_url = reverse_lazy("category_list")


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assets.delete_category"
    raise_exception = True

    model = Category
    template_name = "assets/category_confirm_delete.html"
    success_url = reverse_lazy("category_list")


# ============================================================
# LOCATION VIEWS
# ============================================================

class LocationListView(LoginRequiredMixin, ListView):

    model = Location
    template_name = "assets/location_list.html"
    context_object_name = "locations"

    def get_queryset(self):
        return Location.objects.annotate(asset_count=Count("assets"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_role"] = self.request.user.role if hasattr(self.request.user, "role") else "VIEWER"
        return context


class LocationCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assets.add_location"
    raise_exception = True

    model = Location
    form_class = LocationForm
    template_name = "assets/location_form.html"
    success_url = reverse_lazy("location_list")


class LocationUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assets.change_location"
    raise_exception = True

    model = Location
    form_class = LocationForm
    template_name = "assets/location_form.html"
    success_url = reverse_lazy("location_list")


class LocationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assets.delete_location"
    raise_exception = True

    model = Location
    template_name = "assets/location_confirm_delete.html"
    success_url = reverse_lazy("location_list")


# ============================================================
# USER MANAGEMENT
# ============================================================

class UserListView(PermissionRequiredMixin, ListView):
    permission_required = "assets.view_customuser"
    raise_exception = True

    model = CustomUser
    template_name = "assets/user_list.html"
    context_object_name = "users"


class UserCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "assets.add_customuser"
    raise_exception = True

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "assets/user_form.html"
    success_url = reverse_lazy("user_list")


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "assets.change_customuser"
    raise_exception = True

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "assets/user_form.html"
    success_url = reverse_lazy("user_list")


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "assets.delete_customuser"
    raise_exception = True

    model = CustomUser
    template_name = "assets/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")


# ============================================================
# REPORT VIEWS
# ============================================================

class AssetsByLocationReportView(LoginRequiredMixin, View):

    template_name = "assets/report_assets_by_location.html"

    def get(self, request):
        locations = Location.objects.annotate(asset_count=Count("assets"))
        selected_location = request.GET.get("location")
        assets = None

        if selected_location:
            try:
                location = Location.objects.get(pk=selected_location)
                assets = Asset.objects.filter(location=location).select_related("category", "location")
                context = {
                    "locations": locations,
                    "selected_location": int(selected_location),
                    "assets": assets,
                    "location": location,
                }
                return render(request, self.template_name, context)
            except Location.DoesNotExist:
                messages.error(request, "Selected location does not exist.")

        context = {
            "locations": locations,
            "selected_location": None,
            "assets": assets,
        }
        return render(request, self.template_name, context)

class ExportAssetsByLocationCSV(LoginRequiredMixin, View):
    def get(self, request):
        location_id = request.GET.get('location')
        if not location_id:
            return redirect('report_assets_by_location')
            
        location = get_object_or_404(Location, pk=location_id)
        assets = Asset.objects.filter(location=location).select_related('category')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="assets_at_{location.name.replace(" ", "_")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Serial Number', 'Category', 'Status', 'Purchase Date'])
        
        for asset in assets:
            writer.writerow([
                asset.name,
                asset.serial_number,
                asset.category.name,
                asset.get_status_display(),
                asset.purchase_date
            ])
            
        return response


class LowStockReportView(LoginRequiredMixin, View):

    template_name = "assets/report_low_stock.html"

    def get(self, request):
        low_stock_data = []

        for category in Category.objects.all():
            available_assets = category.assets.filter(status="AVAILABLE")
            available_quantity = available_assets.aggregate(total=Sum("quantity"))["total"] or 0
            
            if available_quantity < category.low_stock_threshold:
                deficit = max(0, category.low_stock_threshold - available_quantity)
                low_stock_data.append({
                    "category": category,
                    "available": available_quantity,
                    "threshold": category.low_stock_threshold,
                    "deficit": deficit,
                    "assets": available_assets[:5],
                })

        context = {"low_stock_items": low_stock_data}
        return render(request, self.template_name, context)

class ExportLowStockCSV(LoginRequiredMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="low_stock_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Category', 'Available', 'Threshold', 'Deficit'])
        
        for category in Category.objects.all():
            available_quantity = category.assets.filter(status="AVAILABLE").aggregate(total=Sum("quantity"))["total"] or 0
            if available_quantity < category.low_stock_threshold:
                deficit = max(0, category.low_stock_threshold - available_quantity)
                
                writer.writerow([
                    category.name,
                    available_quantity,
                    category.low_stock_threshold,
                    deficit
                ])
            
        return response


# ============================================================
# DASHBOARD
# ============================================================

class DashboardView(LoginRequiredMixin, View):
    template_name = "assets/dashboard.html"

    def get(self, request):
        # Basic statistics
        context = {
            "total_assets": Asset.objects.count(),
            "available_assets": Asset.objects.filter(status="AVAILABLE").count(),
            "in_use_assets": Asset.objects.filter(status="IN_USE").count(),
            "in_repair_assets": Asset.objects.filter(status="IN_REPAIR").count(),
            "in_stock_assets": Asset.objects.filter(status="IN_STOCK").count(),
            "total_categories": Category.objects.count(),
            "total_locations": Location.objects.count(),
            "total_users": CustomUser.objects.count(),
            "user_role": request.user.role if hasattr(request.user, "role") else "VIEWER",
        }

        # Low stock summary for dashboard (per category thresholds)
        low_stock_categories = []
        for category in Category.objects.all():
            available_quantity = (
                category.assets.filter(status="AVAILABLE").aggregate(total=Sum("quantity"))[
                    "total"
                ]
                or 0
            )
            if available_quantity < category.low_stock_threshold:
                low_stock_categories.append(
                    {
                        "category": category,
                        "available": available_quantity,
                        "threshold": category.low_stock_threshold,
                    }
                )

        # Recently added assets
        recent_assets = (
            Asset.objects.select_related("category", "location").order_by("-created_at")[:5]
        )

        context["low_stock_categories"] = low_stock_categories
        context["recent_assets"] = recent_assets
        return render(request, self.template_name, context)
