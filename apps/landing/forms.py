from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    """
    Tailwind-styled form for creating and updating featured properties inside the CRM workspace.
    """
    class Meta:
        model = Property
        fields = [
            "image",
            "title",
            "property_type",
            "price",
            "location",
            "description",
            "bedrooms",
            "bathrooms",
            "area_sqft",
            "is_rera_compliant",
            "display_order",
            "is_active",
        ]

        # Shared styling tailwind classes matching the dashboard interface tokens
        INPUT_CLASSES = "w-full p-3 bg-slate-50/50 border border-slate-200 rounded-xl text-sm text-brand-dark placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-orange/20 focus:border-brand-orange transition-all duration-200"
        SELECT_CLASSES = "w-full p-3 bg-slate-50/50 border border-slate-200 rounded-xl text-sm text-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-orange/20 focus:border-brand-orange transition-all duration-200 cursor-pointer"
        TEXTAREA_CLASSES = "w-full p-3 bg-slate-50/50 border border-slate-200 rounded-xl text-sm text-brand-dark placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-orange/20 focus:border-brand-orange transition-all duration-200 resize-none"
        CHECKBOX_CLASSES = "w-5 h-5 rounded border-slate-300 text-brand-orange focus:ring-brand-orange/30 cursor-pointer transition-colors"
        FILE_CLASSES = "w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-orange-50 file:text-brand-orange hover:file:bg-orange-100 cursor-pointer border border-slate-200 rounded-xl p-1.5 bg-slate-50/50 transition-all duration-200"

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "e.g. Prestige Lavender Fields",
                }
            ),
            "property_type": forms.Select(
                attrs={
                    "class": SELECT_CLASSES,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "e.g. 18500000",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "e.g. Whitefield, Bengaluru",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASSES,
                    "rows": 3,
                    "placeholder": "Provide dynamic listing descriptions for home seekers...",
                }
            ),
            "bedrooms": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "min": 0,
                    "placeholder": "BHK Count",
                }
            ),
            "bathrooms": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "min": 0,
                    "placeholder": "Baths Count",
                }
            ),
            "area_sqft": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "placeholder": "e.g. 1800",
                }
            ),
            "is_rera_compliant": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASSES,
                }
            ),
            "display_order": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASSES,
                    "min": 1,
                    "placeholder": "1",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": CHECKBOX_CLASSES,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": FILE_CLASSES,
                    "accept": "image/*",
                }
            ),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_area_sqft(self):
        area = self.cleaned_data.get("area_sqft")
        if area is not None and area <= 0:
            raise forms.ValidationError("Area must be greater than zero.")
        return area