from django import forms

class ListingForm(forms.Form):
    listing_title = forms.CharField(label="listing title",max_length=100)
    listing_price = forms.DecimalField(max_digits=6,decimal_places=2)
    category_choices = [
        ("fashion", "fashion"),
        ("toys", "toys"),
        ("electronics", "electronics"),
        ("home", "home")
    ]
    listing_category = forms.ChoiceField(choices=category_choices, initial="fashion", required=False)
    listing_description = forms.CharField(label="listing description", widget=forms.Textarea)
    img = forms.CharField(label="image url",required=False)

    