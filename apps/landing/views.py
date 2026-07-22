from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView

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

    context = {
        "properties": properties,
    
    }

    return render(
        request,
        "landing/index.html",
        context,
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

        for property in properties:
            data.append({
                "id": property.id,
                "title": property.title,
                "property_type": property.property_type,
                "price": str(property.price),
                "location": property.location,
                "bedrooms": property.bedrooms,
                "bathrooms": property.bathrooms,
                "is_active": property.is_active,
                "display_order": property.display_order,
                "created_at": property.created_at.strftime("%d %b %Y"),
            })

        return JsonResponse({
            "success": True,
            "properties": data,
        })

class PropertyDetailView(DetailView):
    """
    Display property details.
    """

    model = Property
    template_name = "landing/property_detail.html"
    context_object_name = "property"


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

            property = form.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Property created successfully.",
                    "property_id": property.id,
                }
            )

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

        property = get_object_or_404(
            Property,
            pk=pk,
        )

        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property,
        )

        if form.is_valid():

            property = form.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Property updated successfully.",
                    "property_id": property.id,
                }
            )

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

        property = get_object_or_404(
            Property,
            pk=pk,
        )

        property.delete()

        return JsonResponse(
            {
                "success": True,
                "message": "Property deleted successfully.",
            }
        )