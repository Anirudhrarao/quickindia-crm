from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View

from .forms import PropertyForm
from .models import Property


def home(request):
    """
    Render landing page.
    """
    properties = (
        Property.objects
        .filter(is_active=True)
        .order_by("display_order", "-created_at")
    )

    return render(
        request,
        "landing/index.html",
        {
            "properties": properties,
        },
    )


class PropertyListView(View):
    """
    Return all properties as JSON.
    """

    def get(self, request):

        properties = (
            Property.objects
            .order_by("display_order", "-created_at")
        )

        data = []

        for prop in properties:
            data.append({
                "id": prop.id,
                "title": prop.title,
                "property_type": prop.property_type,
                "price": str(prop.price),
                "location": prop.location,
                "description": prop.description,
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "area_sqft": prop.area_sqft,
                "is_rera_compliant": prop.is_rera_compliant,
                "is_active": prop.is_active,
                "display_order": prop.display_order,
                "created_at": prop.created_at.strftime("%d %b %Y"),
            })

        return JsonResponse({
            "success": True,
            "properties": data,
        })


class PropertyDetailView(View):
    """
    Display property details.
    """

    def get(self, request, pk):

        prop = get_object_or_404(
            Property,
            pk=pk,
        )

        # AJAX / JSON request
        if (
            request.headers.get("X-Requested-With") == "XMLHttpRequest"
            or "application/json" in request.headers.get("Accept", "")
        ):
            return JsonResponse({
                "id": prop.id,
                "title": prop.title,
                "property_type": prop.property_type,
                "price": str(prop.price),
                "location": prop.location,
                "description": prop.description,
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "area_sqft": prop.area_sqft,
                "is_rera_compliant": prop.is_rera_compliant,
                "is_active": prop.is_active,
                "display_order": prop.display_order,
            })

        return render(
            request,
            "landing/property_detail.html",
            {
                "property": prop,
            },
        )


class PropertyCreateView(View):
    """
    Create property.
    """

    def post(self, request):

        form = PropertyForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            prop = form.save()

            return JsonResponse({
                "success": True,
                "message": "Property created successfully.",
                "property_id": prop.id,
            })

        return JsonResponse(
            {
                "success": False,
                "errors": form.errors,
            },
            status=400,
        )


class PropertyUpdateView(View):
    """
    Update property.
    """

    def post(self, request, pk):

        prop = get_object_or_404(
            Property,
            pk=pk,
        )

        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=prop,
        )

        if form.is_valid():

            prop = form.save()

            return JsonResponse({
                "success": True,
                "message": "Property updated successfully.",
                "property_id": prop.id,
            })

        return JsonResponse(
            {
                "success": False,
                "errors": form.errors,
            },
            status=400,
        )


class PropertyDeleteView(View):
    """
    Delete property.
    """

    def post(self, request, pk):

        prop = get_object_or_404(
            Property,
            pk=pk,
        )

        prop.delete()

        return JsonResponse({
            "success": True,
            "message": "Property deleted successfully.",
        })